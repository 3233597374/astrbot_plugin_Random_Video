from astrbot.api.star import register, Star, Context
from astrbot.api.event import on_keyword, AstrMessageEvent  # 适配v4.13.1版本，替换filter为on_keyword
import astrbot.api.message_components as Comp
import os
import random  # 新增：导入随机模块


# 插件信息
@register("astrbot_plugin_Random_Video", "榴莲LL", "随机生成各种涩涩视频", "v1.0")
class LocalVideoPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        # ===================== 配置项 =====================
        self.video_folder = "Video"  # 视频文件夹名称（相对于插件根目录）
        # 支持的视频格式（可根据需要添加，如.mov/.avi等）
        self.supported_formats = (".mp4", ".mov", ".avi", ".mkv", ".flv")
        # ==================================================

        # 获取程序根目录
        self.root_dir = os.path.dirname(os.path.abspath(__file__))
        # 拼接Video文件夹完整路径
        self.video_folder_path = os.path.join(self.root_dir, self.video_folder)

    # 新增：获取Video文件夹中的所有视频文件
    def get_all_video_files(self):
        video_files = []
        # 检查Video文件夹是否存在
        if not os.path.exists(self.video_folder_path):
            return video_files

        # 遍历文件夹，筛选视频文件
        for file in os.listdir(self.video_folder_path):
            file_path = os.path.join(self.video_folder_path, file)
            # 只保留文件 + 符合支持的格式
            if os.path.isfile(file_path) and file.lower().endswith(self.supported_formats):
                video_files.append(file_path)
        return video_files

    # 关键词触发：涩涩（适配v4.13.1的on_keyword）
    @on_keyword("涩涩")
    async def on_keyword(self, event: AstrMessageEvent):
        try:
            # 1. 获取所有视频文件
            all_videos = self.get_all_video_files()

            # 2. 检查是否有视频文件
            if not all_videos:
                await event.send(
                    f"Video文件夹中未找到可用视频！\n文件夹路径：{self.video_folder_path}\n支持格式：{self.supported_formats}")
                return

            # 3. 随机选择一个视频
            random_video_path = random.choice(all_videos)

            # 4. 发送随机选中的视频
            await event.send(Comp.Video(file=random_video_path))
            # 可选：发送提示（方便调试）
            # await event.send(f"已发送随机视频：{os.path.basename(random_video_path)}")

        except Exception as e:
            await event.send(f"发送失败：{str(e)}")