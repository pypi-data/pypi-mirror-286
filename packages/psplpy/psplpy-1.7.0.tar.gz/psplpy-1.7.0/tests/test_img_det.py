if __name__ == '__main__':
    from __init__ import *
else:
    from . import *
from psplpyProject.psplpy.image_det import *


def tests():
    image = rc_dir / 'cat.png'
    template_image = rc_dir / 'det_block.png'

    p = PerfCounter()
    result = ImgDet.get_boxes(image, template_image, confidence=0.8, method=ImgDet.TM_CCOEFF_NORMED,
                              draw_result=tmp_dir / 'det_marked.png', save_match=tmp_dir / 'det_match.png')
    p.show('det')
    print(result)
    assert result == [(Rect([(840, 189), (890, 239)], rect_format=Rect.LT_RB), 0.9999983906745911)]


if __name__ == '__main__':
    tests()
