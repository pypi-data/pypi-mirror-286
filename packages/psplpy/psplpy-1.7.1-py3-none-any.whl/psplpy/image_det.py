from pathlib import Path
from typing import Any
import cv2
import numpy as np
from image_utils import ImgConv, Rect


class ImgDet:
    TM_CCOEFF_NORMED = cv2.TM_CCOEFF_NORMED
    TM_CCORR_NORMED = cv2.TM_CCORR_NORMED
    TM_SQDIFF_NORMED = cv2.TM_SQDIFF_NORMED

    @staticmethod
    def _filter_rects(rects: list[Rect], threshold: float) -> list[Rect]:
        """if the two rectangles overlap percentage greater than the threshold, remove the second rectangle"""
        mark_rects = []
        for rect in rects:
            mark_rects.append([rect, True])

        for i in range(len(mark_rects)):
            if mark_rects[i][1]:
                for j in range(i + 1, len(mark_rects)):
                    if mark_rects[j][1]:
                        overlap_ratio = max(mark_rects[i][0].overlap_pct(mark_rects[j][0]))
                        if overlap_ratio >= threshold:
                            mark_rects[j][1] = False

        return [rect[0] for rect in mark_rects if rect[1]]

    @staticmethod
    def _get_result(image: Any, template_image: Any, method: int = cv2.TM_CCOEFF_NORMED, save_match: Path | str = None):
        cvt_image = ImgConv(image).to_opencv()
        cvt_template_image = ImgConv(template_image).to_opencv()
        result = cv2.matchTemplate(cvt_image, cvt_template_image, method)  # 使用模板匹配
        if method == ImgDet.TM_SQDIFF_NORMED:
            result = -((result - 0.5) * 2)
        if save_match is not None:
            result_copy = result.copy()
            result_copy = ((result_copy + 1) * (255 / 2)).astype(np.uint8)
            cv2.imwrite(str(save_match), result_copy)
        return result, cvt_image, cvt_template_image

    @staticmethod
    def _draw_result(cvt_image: np.ndarray, rects: list[Rect], path: Path | str) -> None:
        copied_image = cvt_image.copy()
        for rect in rects:
            cv2.rectangle(copied_image, rect[0], rect[1], (0, 0, 255), 1)
        cv2.imwrite(str(path), copied_image)

    @staticmethod
    def get_box(image: Any, template_image: Any, confidence: float = 0.9, method: int = cv2.TM_CCOEFF_NORMED,
                draw_result: Path | str = None, save_match: Path | str = None) -> tuple[Rect, float] | None:
        result, cvt_image, cvt_template_image = ImgDet._get_result(image, template_image, method, save_match)

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val < confidence:
            return None
        top_left = max_loc
        h, w = cvt_template_image.shape[:2]
        bottom_right = (top_left[0] + w, top_left[1] + h)
        rect = Rect((top_left, bottom_right), rect_format=Rect.LT_RB)
        if draw_result is not None:
            ImgDet._draw_result(cvt_image, [rect], draw_result)
        return rect, float(result[max_loc[::-1]])

    @staticmethod
    def get_boxes(image: Any, template_image: Any, confidence: float = 0.9, overlap: float = 0.5,
                  method: int = cv2.TM_CCOEFF_NORMED, draw_result: Path | str = None,
                  save_match: Path | str = None) -> list[tuple[Rect, float]]:
        """return_data_structure: [(Rect1, confidence1), (Rect2, confidence2), ...] or []"""
        result, cvt_image, cvt_template_image = ImgDet._get_result(image, template_image, method, save_match)

        indices = np.where(result >= confidence)
        positions = np.column_stack(indices)
        sorted_positions = np.argsort(result[indices])[::-1]  # sort in descending order
        sorted_positions = [sorted_position[::-1] for sorted_position in positions[sorted_positions]]
        boxes = []
        h, w = cvt_template_image.shape[:2]
        for top_left in sorted_positions:
            bottom_right = [top_left[0] + w, top_left[1] + h]
            boxes.append(Rect([top_left, bottom_right], rect_format=Rect.LT_RB))
        if overlap:
            boxes = ImgDet._filter_rects(boxes, overlap)
        rects = [(box, float(result[box[0][::-1]])) for box in boxes]
        if draw_result is not None:
            ImgDet._draw_result(cvt_image, [rect[0] for rect in rects], draw_result)
        return rects

    @staticmethod
    def det_img(image: Any, template_image: Any, confidence: float = 0.9, method: int = cv2.TM_CCOEFF_NORMED,
                draw_result: Path | str = None, save_match: Path | str = None) -> bool:
        return bool(ImgDet.get_box(image, template_image, confidence, method, draw_result, save_match))
