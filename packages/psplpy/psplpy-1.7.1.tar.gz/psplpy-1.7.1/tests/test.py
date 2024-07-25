if __name__ == '__main__':
    import test_middleware_utils
    import test_serialization_utils
    import test_concurrency_utils
    import test_network_utils
    import test_file_utils
    import test_image_utils
    import test_other_utils
    import test_dynamic_compose
    import test_ocr_utils
    import test_img_det
else:
    from . import test_middleware_utils
    from . import test_serialization_utils
    from . import test_concurrency_utils
    from . import test_network_utils
    from . import test_file_utils
    from . import test_image_utils
    from . import test_other_utils
    from . import test_dynamic_compose
    from . import test_ocr_utils
    from . import test_img_det


def global_test():
    test_middleware_utils.tests()
    test_serialization_utils.tests()
    test_concurrency_utils.tests()
    test_network_utils.tests()
    test_file_utils.tests()
    test_image_utils.tests()
    test_other_utils.tests()
    test_dynamic_compose.tests()
    test_ocr_utils.tests()
    test_img_det.tests()


if __name__ == '__main__':
    global_test()
