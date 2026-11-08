# GitHub 上传与课程提交

提交对象是包含 README、四项任务代码、俄语报告和控制题答案的 **GitHub 仓库主页链接**。Docker Hub 地址用于证明任务 2 的镜像发布。下面两种上传方式任选一种。

## 方式一 · 在 GitHub 网页上传

1. 解压项目包，打开包含 `README.md` 的 `bsu-niispo-lab1-group13` 文件夹。如果刚解压完看到的仍然是一个同名文件夹，再打开一层。
2. 登录自己的 GitHub 账号，创建仓库，名称可用 `bsu-niispo-lab1-group13`。根据课程要求选择可见性。选私有时，需在仓库设置的 `Collaborators` 中邀请老师，并由老师接受。新建仓库时跳过 README、.gitignore 和许可证，直接创建空仓库。[新建 GitHub 仓库](https://github.com/new)
3. 在空仓库首页点击 **uploading an existing file**。有内容的仓库可通过 **Add file → Upload files** 进入。将解压目录里的 `task1`、`task2`、`task3`、`task4`、`docs`、`README.md` 和 `.gitignore` 拖入页面。拖入的是项目目录**里面的内容**，这样 GitHub 首页就会直接显示 README。
4. 检查准备提交的文件列表，尤其是 `.gitignore` 和 `task4/compose/.env.example`。如果浏览器跳过了点号开头的文件，可先完成其他文件的提交，再用 **Add file → Create new file**，输入对应的完整相对路径，从解压包的同名文件复制内容并提交。真实的 `.env` 仅保存在电脑上。网页上传不会替你按 `.gitignore` 过滤文件，请使用刚解压的干净目录。
5. 填写提交说明，例如 `Add Docker lab 1, tasks 1-4 and report`，点击 **Commit changes** 并确认。刷新仓库首页，确认可以从 README 打开俄语报告和 32 题答案。也可以按下文“提交前核对”检查目录。[GitHub 网页上传说明](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository)

## 方式二 · 使用 Git for Windows 和 PowerShell

先按方式一的第 2 步建立**空仓库**。在仓库的 **Quick setup** 中选择 **HTTPS** 并复制以 `.git` 结尾的地址。打开解压后**含 README 的文件夹**，在资源管理器地址栏输入 `powershell` 并回车。在这个窗口中执行以下命令。如果 `git --version` 无法识别，安装 Git for Windows 后重新打开窗口，或选择上面的网页方式。[Git for Windows](https://git-scm.com/downloads/win)

```powershell
git --version
git init -b main
git status --short
```

首次使用 Git，可执行以下两行，按提示输入提交署名和你选择公开的提交邮箱。设置仅用于当前仓库，也可以使用 GitHub 邮箱设置页面提供的 noreply 地址。

```powershell
git config user.name (Read-Host "Commit author name")
git config user.email (Read-Host "Commit email")
```

再执行以下命令。`Read-Host` 提示出现时粘贴**自己刚复制的真实仓库地址**。

```powershell
git add .
git diff --cached --name-only
git commit -m "Add Docker lab 1, tasks 1-4 and report"
$repoUrl = Read-Host "Paste the HTTPS clone URL from GitHub"
git remote add origin $repoUrl
git remote -v
git push -u origin main
```

检查暂存文件时应能看到 `.gitignore`、`task4/compose/.env.example`，以及 `docs/report.md`。如果列表里出现真实 `.env`，先停止提交并检查项目根目录中的 `.gitignore`。Windows 通常可通过 Git Credential Manager 打开浏览器完成 GitHub 登录。若命令行通过 HTTPS 提示输入密码，GitHub 要求使用个人访问令牌（PAT），账号登录密码不能用于 Git 操作。令牌只在认证提示中输入。[GitHub 命令行上传说明](https://docs.github.com/en/migrations/importing-source-code/using-the-command-line-to-import-source-code/adding-locally-hosted-code-to-github) · [远端与认证](https://docs.github.com/en/get-started/git-basics/about-remote-repositories)

如果 `origin already exists`，先用 `git remote -v` 检查目标，确实需要换仓库时使用 `git remote set-url origin $repoUrl`。如果目标仓库已有提交，最简单的办法是单独克隆它，将解压目录的内容复制到克隆目录，再执行 `git add .`、`git commit` 和 `git push`。保留远端历史即可。

## 提交前核对

- GitHub 首页直接显示 `README.md` 和 `task1` 至 `task4`。报告链接能打开 `docs/report.md`，控制题文件有 1–32 题。
- 在报告中打开一次 Compose 原实验截图和镜像大小记录，确认附件已一起上传。
- 公共仓库可在未登录的浏览器中验证链接。私有仓库请确认老师的账号已获得访问权限。
- 从浏览器地址栏复制仓库**主页**地址，格式为 `https://github.com/你的GitHub用户名/你的仓库名`。将实际地址粘贴到学校教学平台该实验的答案栏并提交。课上可从 README 的任务 4 快速演示开始。

**Для учебного портала.** Опубликуйте распакованные файлы в репозитории GitHub. Откройте отчёт по ссылке в README, проверьте доступ преподавателя и отправьте на учебный портал адрес главной страницы репозитория.
