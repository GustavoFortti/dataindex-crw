page_arguments = {
    "name": "a1supplements",
    "url": "https://a1supplements.com",
    "brand": "a1supplements",
    "page_production_status": True,
    "crawler_driver_user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "affiliate_url": None,
    "affiliate_coupon_discount_percentage": None,
    "affiliate_coupon": None,
    "html_metadata_type": ["text", "image"],
    "html_description_path": [
        {'tag': None, 'path': '#tab-description'},
        {
            'tag': None,
            'path': (
                '#ProductInfo-template--22993487429938__main > '
                'div.product__description.rte.quick-add-hidden'
            ),
        },
        {
            'tag': None,
            'path': (
                '#MainProduct-template--22993487429938__main > '
                'div.product.product--large.product--left.product--thumbnail_slider'
                '.product--mobile-show.grid.grid--1-col.grid--2-col-tablet > '
                'div.grid__item.product__media-wrapper > div.MainAccordionSection.workOnlyDesktop'
            ),
        },
    ],
    "html_images_list": [
        {
            'tag': None,
            'path': (
                '#MainProduct-template--22993487429938__main > '
                'div.product.product--large.product--left.product--thumbnail_slider'
                '.product--mobile-show.grid.grid--1-col.grid--2-col-tablet > '
                'div.grid__item.product__media-wrapper > div.MainMEdiaWrapper > '
                'div.CustomThumbnailWrapper > div > div > div'
            ),
        },
    ],
    "html_remove_first_image_from_list": True,
    "html_dynamic_scroll": {
        "start_time_sleep": 3,
        "time_sleep": 0.5,
        "scroll_step": 1000,
        "percentage": 0.07,
        "return_percentage": 0.3,
        "max_return": 4000,
        "max_attempts": 3,
    },
}