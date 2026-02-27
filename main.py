from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import register, Star, Context
import astrbot.api.message_components as Comp
import os
import random


# 插件信息
@register("astrbot_plugin_Random_Video", "榴莲LL", "随机生成各种涩涩视频", "v1.0", "")
class LocalVideoPlugin(Star):
    def __init__(self, context: Context, config=None):
        super().__init__(context)
        self.config = config or {}

        self.video_folder = self.config.get("video_folder", "Video")
        # 支持的视频格式
        self.supported_formats = tuple(self.config.get("supported_formats", [".mp4", ".mov", ".avi", ".mkv", ".flv"]))
        # ==================================================

        # 获取插件根目录
        self.plugin_root = os.path.dirname(os.path.abspath(__file__))
        # 拼接Video文件夹完整路径
        self.video_folder_path = os.path.join(self.plugin_root, self.video_folder)

    @filter.command("涩涩", alias={'ss', '涩涩视频'})
    async def random_video_handler(self, event: AstrMessageEvent):
        """
        关键词触发的核心处理函数
        """
        try:
            # 获取所有视频文件
            all_videos = self.get_all_video_files()

            # 检查是否有视频文件
            if not all_videos:
                error_msg = (
                    f"❌ Video文件夹中未找到可用视频！\n"
                    f"📁 文件夹路径：{self.video_folder_path}\n"
                    f"🔍 支持格式：{self.supported_formats}"
                )
                yield event.plain_result(error_msg)
                return

            # 随机选择一个视频
            random_video_path = random.choice(all_videos)

            # 发送随机选中的视频
            yield event.chain_result([
                Comp.Video(file=random_video_path),
                Comp.Plain(f"✅ 已发送随机视频：{os.path.basename(random_video_path)}")
            ])

        except Exception as e:
            yield event.plain_result(f"⚠️ 发送失败：{str(e)}")

    # 获取Video文件夹中的所有视频文件
    def get_all_video_files(self):
        video_files = []
        # 检查Video文件夹是否存在
        if not os.path.exists(self.video_folder_path):
            # 自动创建空文件夹，避免首次使用报错
            os.makedirs(self.video_folder_path, exist_ok=True)
            return video_files

        # 遍历文件夹，筛选视频文件
        try:
            for file in os.listdir(self.video_folder_path):
                file_path = os.path.join(self.video_folder_path, file)
                if os.path.isfile(file_path) and file.lower().endswith(self.supported_formats):
                    video_files.append(file_path)
        except PermissionError:
            # 处理文件夹权限问题
            return []

        return video_files

    # 增加插件卸载清理
    async def terminate(self):
        """插件卸载时的清理操作"""
        pass