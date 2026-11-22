# HF Notes

一个部署在 GitHub Pages 上的轻量中文个人博客。网站没有依赖包、广告、统计脚本或远程字体。

## 修改内容

编辑 `content.json`：`site` 保存博客名字与简介；`posts` 保存文章。每篇文章有唯一的 `slug`、标题、分类、日期、摘要和若干段落。

```powershell
python build.py
python -m http.server 4173
```

打开 http://localhost:4173 预览。运行生成器后，连同生成的 HTML、RSS、站点地图和源文件一起提交到 `main`，GitHub Pages 即可发布。不要只修改生成的 HTML，否则下次生成时会被覆盖。

## 发布

仓库 Settings → Pages 的发布来源使用 `main` 分支的根目录。无需数据库或另外租用服务器。

## 公开内容

第一版只使用这次建站对话中已确认的信息：创建个人博客、使用 GitHub Pages、希望记录学习与尝试，并保留未公开项目的细节。未推测或添加真实姓名、联系方式、学校、公司、所在地、任职或项目业绩。开站文章由 AI 根据本次对话协助起草，可继续修改。

所有随仓库提交的文件都可公开访问。不要把私人笔记、身份资料、密钥、内部文档或未公开项目实现加入这个仓库。

## 设计与图片

设计方向参考 [Refero / Apple](https://styles.refero.design/style/aecac5da-f397-4ddf-b71f-de1efc434cb8)，已按中文博客重新排版。

封面为 Unsplash 产品摄影，非博主个人照片。图片源：https://images.unsplash.com/photo-1496181133206-80ce9b88a853 。本地版本仅做格式与尺寸优化，依据 [Unsplash License](https://unsplash.com/license) 使用。
