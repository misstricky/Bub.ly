key                           -                   data
==================================================================
counter:user                  -                   1
user:email:<md5(email)>       -                 <user_id>  eg: 1
user:apikey:<xxx>             -                 <user_id>  eg: 1
user:<user_id>                -   hash {"email": "some@some.com",
                                       "password": "s3fdd$jlh32hwk32k23k",
                                       "api_key": "xxxxxxxxx",
                                       "custom_domain": "http://t.co/"}
user:urls:<user_id>           -      [14345, 14899, 15234, 19002] -> list


counter:url                   -         14000
url:<url_id>                  -   hash {"url": "http://google.com/",
                                        "hits": 0,
                                        "created_at": "1281778154.86",
                                        "is_file": False,
                                        "file_name": "some.jpg"}

                                       


