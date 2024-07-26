
from typing import Union
from cobweb import setting
from cobweb.utils import OssUtil
from cobweb.crawlers import Crawler
from cobweb.base import Seed, BaseItem, Request, Response
from cobweb.exceptions import OssDBPutPartError, OssDBMergeError


oss_util = OssUtil()


class FileCrawlerAir(Crawler):

    @staticmethod
    def download(item: Request) -> Union[Seed, BaseItem, Response, str]:
        seed_dict = item.seed.to_dict
        bucket_name = oss_util.bucket
        try:
            key = item.seed.oss_path
            if oss_util.exists(key):
                content_length = oss_util.head(key).content_length
                yield Response(item.seed, "exists", bucket_name=bucket_name, data_size=content_length, **seed_dict)

            end = seed_dict.get("end", "")
            start = seed_dict.get("start", "0")

            if end or int(start):
                item.request_setting["headers"]['Range'] = f'bytes={start}-{end}'

            if not item.seed.params.identifier:
                content = b""
                chunk_size = oss_util.chunk_size
                min_upload_size = oss_util.min_upload_size
                position = seed_dict.get("position", 1)

                response = item.download()

                content_length = int(response.headers.get("content-length", 0))
                content_type = response.headers.get("content-type", "").split(";")[0]
                if content_type and content_type in setting.FILE_FILTER_CONTENT_TYPE:
                    yield Response(
                        item.seed, response, filter=True, msg=f"response content type is {content_type}",
                        bucket_name=bucket_name, data_size=content_length, **seed_dict
                    )
                elif position == 1 and min_upload_size >= content_length > 0:
                    """过小文件标识返回"""
                    yield Response(
                        item.seed, response, filter=True, msg="file size is too small",
                        bucket_name=bucket_name, data_size=content_length, **seed_dict
                    )
                elif position == 1 and chunk_size > content_length > min_upload_size:
                    """小文件直接下载"""
                    for part_data in response.iter_content(chunk_size):
                        content += part_data
                    oss_util.put(key, content)
                    yield Response(item.seed, response, bucket_name=bucket_name, data_size=content_length, **seed_dict)
                    response.close()
                else:
                    """中大文件同步分片下载"""
                    upload_content_length = 0
                    if not seed_dict.get("upload_id"):
                        seed_dict["upload_id"] = oss_util.init_part(key).upload_id
                    upload_id = seed_dict["upload_id"]
                    for part_data in response.iter_content(chunk_size):
                        content += part_data
                        if len(content) >= chunk_size:
                            upload_data = content[:chunk_size]
                            content = content[chunk_size:]
                            oss_util.put_part(key, upload_id, position, upload_data)
                            upload_content_length += len(upload_data)
                            position += 1
                            seed_dict['position'] = position
                            seed_dict['start'] = upload_content_length

                    response.close()
                    if content:
                        oss_util.put_part(key, upload_id, position, content)
                        content_length += len(content)
                    oss_util.merge(key, upload_id)
                    yield Response(item.seed, response, bucket_name=bucket_name, data_size=content_length, **seed_dict)

            elif item.seed.params.identifier == "merge":
                oss_util.merge(key, seed_dict["upload_id"])
                content_length = oss_util.head(key).content_length
                yield Response(item.seed, "merge", bucket_name=bucket_name, data_size=content_length, **seed_dict)
        except OssDBPutPartError:
            yield Seed(seed_dict)
        except OssDBMergeError:
            yield Seed(seed_dict, identifier="merge")


class FileCrawlerPro(Crawler):

    @staticmethod
    def download(item: Request) -> Union[Seed, BaseItem, Response, str]:
        seed_dict = item.seed.to_dict
        bucket_name = oss_util.bucket
        try:
            key = item.seed.oss_path
            if oss_util.exists(key):
                content_length = oss_util.head(key).content_length
                yield Response(item.seed, "exists", bucket_name=bucket_name, data_size=content_length, **seed_dict)

            end = seed_dict.get("end", "")
            start = seed_dict.get("start", "0")

            if end or int(start):
                item.request_setting["headers"]['Range'] = f'bytes={start}-{end}'

            if not item.seed.params.identifier:
                content = b""
                chunk_size = oss_util.chunk_size
                min_upload_size = oss_util.min_upload_size
                position = seed_dict.get("position", 1)

                response = item.download()

                content_length = int(response.headers.get("content-length", 0))
                content_type = response.headers.get("content-type", "").split(";")[0]
                if content_type and content_type in setting.FILE_FILTER_CONTENT_TYPE:
                    yield Response(
                        item.seed, response, filter=True, msg=f"response content type is {content_type}",
                        bucket_name=bucket_name, data_size=content_length, **seed_dict
                    )
                elif position == 1 and min_upload_size >= content_length > 0:
                    """过小文件标识返回"""
                    yield Response(
                        item.seed, response, filter=True, msg="file size is too small",
                        bucket_name=bucket_name, data_size=content_length, **seed_dict
                    )
                elif position == 1 and chunk_size > content_length > min_upload_size:
                    """小文件直接下载"""
                    for part_data in response.iter_content(chunk_size):
                        content += part_data
                    oss_util.put(key, content)
                    yield Response(item.seed, response, bucket_name=bucket_name, data_size=content_length, **seed_dict)
                    response.close()
                else:
                    """中大文件同步分片下载"""
                    upload_content_length = 0
                    if not seed_dict.get("upload_id"):
                        seed_dict["upload_id"] = oss_util.init_part(key).upload_id
                    upload_id = seed_dict["upload_id"]
                    for part_data in response.iter_content(chunk_size):
                        content += part_data
                        if len(content) >= chunk_size:
                            upload_data = content[:chunk_size]
                            content = content[chunk_size:]
                            oss_util.put_part(key, upload_id, position, upload_data)
                            upload_content_length += len(upload_data)
                            position += 1
                            seed_dict['position'] = position
                            seed_dict['start'] = upload_content_length

                    response.close()
                    if content:
                        oss_util.put_part(key, upload_id, position, content)
                        content_length += len(content)
                    oss_util.merge(key, upload_id)
                    yield Response(item.seed, response, bucket_name=bucket_name, data_size=content_length, **seed_dict)

            elif item.seed.params.identifier == "merge":
                oss_util.merge(key, seed_dict["upload_id"])
                content_length = oss_util.head(key).content_length
                yield Response(item.seed, "merge", bucket_name=bucket_name, data_size=content_length, **seed_dict)

        except OssDBPutPartError:
            yield Seed(seed_dict)
        except OssDBMergeError:
            yield Seed(seed_dict, identifier="merge")
