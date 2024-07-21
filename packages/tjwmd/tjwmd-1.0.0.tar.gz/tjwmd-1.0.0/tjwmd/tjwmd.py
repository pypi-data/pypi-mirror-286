import math
from typing import List

import cv2
import numpy as np
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator


class TJWMD:
    def __init__(
            self,
            wm_counter_model: YOLO,
            wm_counter_labels: List[str],
            wm_digits_model: YOLO,
    ):
        self.wm_counter_model = wm_counter_model
        self.wm_counter_labels = wm_counter_labels
        self.wm_digits_model = wm_digits_model

    @staticmethod
    def _rotate_image_to_zero(frame, angle_: float):
        (h, w) = frame.shape[:2]

        center = (w // 2, h // 2)

        M = cv2.getRotationMatrix2D(center, -angle_, 1.0)

        cos = np.abs(M[0, 0])
        sin = np.abs(M[0, 1])
        new_w = int((h * sin) + (w * cos))
        new_h = int((h * cos) + (w * sin))

        M[0, 2] += (new_w / 2) - center[0]
        M[1, 2] += (new_h / 2) - center[1]

        rotated_frame = cv2.warpAffine(frame, M, (new_w, new_h))

        return rotated_frame

    @staticmethod
    def _resize_frame(
            frame, max_width: int = 640, max_height: int = 640
    ):
        original_height, original_width = frame.shape[:2]

        width_ratio = max_width / original_width
        height_ratio = max_height / original_height

        min_ratio = min(width_ratio, height_ratio)

        new_width = int(original_width * min_ratio)
        new_height = int(original_height * min_ratio)

        return cv2.resize(frame, (new_width, new_height))

    def _detect_counters(
            self,
            frame_,
            conf: float = 0.1
    ):
        results = self.wm_counter_model.predict(
            source=frame_,
            conf=conf
        )

        bboxes = []
        for result in results:
            boxes = result.boxes
            for box in boxes:
                c = box.cls
                if self.wm_counter_model.names[int(c)] in self.wm_counter_labels:
                    bboxes.append(box.xyxy[0])

        return bboxes

    @staticmethod
    def _is_center_inside_box(center, bbox):
        x_center, y_center = center
        x_min, y_min, x_max, y_max = bbox
        return x_min <= x_center <= x_max and y_min <= y_center <= y_max

    @staticmethod
    def _calculate_bbox_center(bbox):
        return (
            (bbox[0] + bbox[2]) / 2,
            (bbox[1] + bbox[3]) / 2
        )

    @staticmethod
    def _get_bbox_h_w(bbox):
        return bbox[3] - bbox[1], bbox[2] - bbox[0]

    @staticmethod
    def _remove_invalid_counters(counters):
        if len(counters) == 0:
            return counters

        valid_counters = []
        prev_counter = None
        for counter in counters:
            h, w = TJWMD._get_bbox_h_w(counter)
            if h > w:
                continue

            if prev_counter is None:
                prev_counter = counter
                valid_counters.append(prev_counter)
                continue

            center = TJWMD._calculate_bbox_center(counter)
            if TJWMD._is_center_inside_box(center, prev_counter):
                continue

            valid_counters.append(prev_counter)
            prev_counter = counter

        return valid_counters

    def _detect_digits(
            self,
            frame_,
            conf: float = 0.1,
    ):
        results = self.wm_digits_model.predict(
            source=frame_,
            conf=conf
        )

        digits = []
        for result in results:
            boxes = result.boxes
            for box in boxes:
                c = box.cls
                digits.append((box.xyxy[0], self.wm_digits_model.names[int(c)]))

        return digits

    @staticmethod
    def _get_midpoint(point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        midpoint = ((x1 + x2) / 2, (y1 + y2) / 2)
        return midpoint

    @staticmethod
    def _angle_with_center(point, center):
        x, y = point
        cx, cy = center
        angle_radian = math.atan2(y - cy, x - cx)
        angle_degree = math.degrees(angle_radian)
        if angle_degree < 0:
            angle_degree += 360
        return angle_degree

    def predict(
            self,
            frame_,
            num_of_digits: int,
            wm_counter_conf: float = 0.1,
            wm_digits_conf: float = 0.1,
            angle: float = None,
    ):
        resized_frame = self._resize_frame(frame_, max_width=640, max_height=640)
        if angle is not None:
            resized_frame = self._rotate_image_to_zero(resized_frame, angle)

        drawing_frame = resized_frame.copy()

        counters = self._detect_counters(resized_frame, wm_counter_conf)
        counters = self._remove_invalid_counters(counters)
        if not counters:
            return []

        values = []
        for counter in counters:
            digits = self._detect_digits(resized_frame, wm_digits_conf)
            digits = list(sorted(digits, key=lambda x: x[0][0]))

            prev_digit = None
            valid_digits = []
            for digit in digits:
                bbox, label = digit
                center = TJWMD._calculate_bbox_center(bbox)

                if not TJWMD._is_center_inside_box(center, counter):
                    continue

                if prev_digit is None:
                    prev_digit = digit
                    valid_digits.append(digit)
                    continue

                if TJWMD._is_center_inside_box(center, prev_digit[0]):
                    continue

                prev_digit_center = TJWMD._calculate_bbox_center(prev_digit[0])
                midpoint = TJWMD._get_midpoint(prev_digit_center, center)
                check_point = center if center[1] > prev_digit_center[1] else prev_digit_center
                angle = TJWMD._angle_with_center(check_point, midpoint)
                if 45 <= angle <= 135:
                    continue

                prev_digit = digit
                valid_digits.append(digit)

            if len(valid_digits) == num_of_digits:
                annotator = Annotator(drawing_frame)
                annotator.box_label(counter)
                for digit in valid_digits:
                    annotator.box_label(digit[0], digit[1])
                values.append("".join([digit[1] for digit in valid_digits]))

        return values, drawing_frame
