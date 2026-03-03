简单直接的回答：**第一阶段的循环卸载命令（for 循环）可以尝试，但通常不建议新手直接“盲跑”所有命令**，因为在 Ubuntu 中彻底移除 Snap 是一项“外科手术式”的操作，一旦出错，可能会导致你的桌面环境（GNOME）部分功能异常。

为了确保安全，我建议你按照以下修正后的**“半手动”流程**操作，这样最稳妥：

### 1. 为什么不能“一键全删”？

你的截图显示你有 `gnome-46-2404` 等核心组件。如果强行用脚本瞬间删除所有 Snap，可能会导致：

- **应用中心 (Snap Store)** 消失后，你没有图形化的软件安装工具。
    
- **Firefox** 立即无法使用（它是 Ubuntu 默认唯一的浏览器）。
    
- **主题和图标** 变丑（依赖 `gtk-common-themes`）。
    

---

### 2. 建议的操作顺序（请按此执行）

#### 第一步：先装好“救命”的浏览器

在删 Snap 之前，必须先有一个能用的 `.deb` 版浏览器，否则你会陷入没法上网查资料的窘境。

Bash

```
sudo add-apt-repository ppa:mozillateam/ppa -y
sudo apt update
sudo apt install firefox -y
```

#### 第二步：手动卸载应用类 Snap

先卸载你看得见的应用，最后卸载系统核心组件。请依次执行：

Bash

```
# 卸载商店和固件更新器
sudo snap remove --purge snap-store
sudo snap remove --purge firefox
sudo snap remove --purge firmware-updater
sudo snap remove --purge snapd-desktop-integration
```

#### 第三步：清理剩余的“骨架”

此时你可以运行那个循环命令来清理剩下的 `core` 和 `gnome` 平台库：

Bash

```
for s in $(snap list | awk '!/^Name|^内容/ {print $1}'); do
    sudo snap remove --purge "$s"
done
```

_如果报错说某个包被依赖（如 `core24`），没关系，多运行两次，它会自动从外层往里层拆解。_

#### 第四步：送走 snapd 服务

当 `snap list` 结果为空时，执行：

Bash

```
sudo apt autoremove --purge snapd
rm -rf ~/snap
sudo rm -rf /snap
sudo rm -rf /var/lib/snapd
```

---

### 3. 最关键的一步：锁死 Snap

如果你不执行这一步，下次你执行 `apt upgrade` 时，Ubuntu 可能会为了安装某个依赖包又把 `snapd` 偷偷装回来。

Bash

```
sudo nano /etc/apt/preferences.d/nosnap.pref
```

把这段话粘贴进去并保存：

Plaintext

```
Package: snapd
Pin: release a=*
Pin-Priority: -10
```

---

### 总结建议

**你可以用这些命令，但请先确保安装好了 `.deb` 版的 Firefox。**

移除 Snap 后，你的系统盘（80G）会立刻释放出大约 2GB-4GB 的空间，且 `lsblk` 命令下那一大串 `loop` 设备也会消失，清爽很多。

**操作完后，需要我教你如何安装 Flatpak 吗？它是 Snap 的完美替代品，且不会像 Snap 这样强行挂载一堆设备。**简单直接的回答：**第一阶段的循环卸载命令（for 循环）可以尝试，但通常不建议新手直接“盲跑”所有命令**，因为在 Ubuntu 中彻底移除 Snap 是一项“外科手术式”的操作，一旦出错，可能会导致你的桌面环境（GNOME）部分功能异常。

为了确保安全，我建议你按照以下修正后的**“半手动”流程**操作，这样最稳妥：

### 1. 为什么不能“一键全删”？

你的截图显示你有 `gnome-46-2404` 等核心组件。如果强行用脚本瞬间删除所有 Snap，可能会导致：

- **应用中心 (Snap Store)** 消失后，你没有图形化的软件安装工具。
    
- **Firefox** 立即无法使用（它是 Ubuntu 默认唯一的浏览器）。
    
- **主题和图标** 变丑（依赖 `gtk-common-themes`）。
    

---

### 2. 建议的操作顺序（请按此执行）

#### 第一步：先装好“救命”的浏览器

在删 Snap 之前，必须先有一个能用的 `.deb` 版浏览器，否则你会陷入没法上网查资料的窘境。

Bash

```
sudo add-apt-repository ppa:mozillateam/ppa -y
sudo apt update
sudo apt install firefox -y
```

#### 第二步：手动卸载应用类 Snap

先卸载你看得见的应用，最后卸载系统核心组件。请依次执行：

Bash

```
# 卸载商店和固件更新器
sudo snap remove --purge snap-store
sudo snap remove --purge firefox
sudo snap remove --purge firmware-updater
sudo snap remove --purge snapd-desktop-integration
```

#### 第三步：清理剩余的“骨架”

此时你可以运行那个循环命令来清理剩下的 `core` 和 `gnome` 平台库：

Bash

```
for s in $(snap list | awk '!/^Name|^内容/ {print $1}'); do
    sudo snap remove --purge "$s"
done
```

_如果报错说某个包被依赖（如 `core24`），没关系，多运行两次，它会自动从外层往里层拆解。_

#### 第四步：送走 snapd 服务

当 `snap list` 结果为空时，执行：

Bash

```
sudo apt autoremove --purge snapd
rm -rf ~/snap
sudo rm -rf /snap
sudo rm -rf /var/lib/snapd
```

---

### 3. 最关键的一步：锁死 Snap

如果你不执行这一步，下次你执行 `apt upgrade` 时，Ubuntu 可能会为了安装某个依赖包又把 `snapd` 偷偷装回来。

Bash

```
sudo nano /etc/apt/preferences.d/nosnap.pref
```

把这段话粘贴进去并保存：

Plaintext

```
Package: snapd
Pin: release a=*
Pin-Priority: -10
```

---

### 总结建议

**你可以用这些命令，但请先确保安装好了 `.deb` 版的 Firefox。**

移除 Snap 后，你的系统盘（80G）会立刻释放出大约 2GB-4GB 的空间，且 `lsblk` 命令下那一大串 `loop` 设备也会消失，清爽很多。

