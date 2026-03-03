# Linux 进阶学习计划

**学习周期**：12周（约3个月）  
**目标**：从日常用户进阶为Linux技术达人

---

## 阶段一：Shell脚本进阶（第1-4周）

### 第1周：基础巩固
- **内容**：
  - Bash基本语法复习
  - 变量、条件判断、循环
  - 函数定义与调用
- **实践**：写一个自动备份脚本
- **资源**：《Linux命令行与shell脚本编程大全》前6章

### 第2周：文本处理
- **内容**：
  - grep, sed, awk 三大剑客
  - 正则表达式
  - 管道与重定向进阶
- **实践**：日志分析脚本
- **资源**：[Linux文本处理三剑客](https://github.com/trimstray/the-book-of-secret-knowledge)

### 第3周：系统管理脚本
- **内容**：
  - 磁盘/内存/CPU监控
  - 用户管理自动化
  - 定时任务crontab深入
- **实践**：服务器健康监控脚本
- **资源**：《Linux高性能服务器编程》

### 第4周：项目实战
- **实践项目**：
  - 自动部署脚本
  - 日志轮转与清理脚本
  - 批量操作工具

---

## 阶段二：Linux内核原理（第5-8周）

### 第5周：内核简介与编译
- **内容**：
  - Linux内核架构
  - 内核源码目录结构
  - 编译自己的内核
- **实践**：在虚拟机编译一个精简内核
- **资源**：《深入理解Linux内核》

### 第6周：进程管理
- **内容**：
  - 进程调度原理
  - PCB与task_struct
  - 上下文切换
- **实践**：用top/htop分析进程
- **资源**：[Linux-insides](https://github.com/0xAX/linux-insides)

### 第7周：内存管理
- **内容**：
  - 虚拟内存原理
  - 页面置换算法
  - slab分配器
- **实践**：分析/proc/meminfo

### 第8周：文件系统与网络
- **内容**：
  - VFS虚拟文件系统
  - ext4/xfs原理
  - 网络协议栈初探

---

## 阶段三：系统调优（第9-12周）

### 第9周：性能监控
- **内容**：
  - perf性能分析
  - strace/ltrace调试
  - vmstat/iostat/sar
- **实践**：分析一个实际性能问题

### 第10周：内核参数调优
- **内容**：
  - sysctl参数详解
  - 网络参数优化
  - 文件描述符限制
- **实践**：根据业务场景调优

### 第11周：容器与虚拟化
- **内容**：
  - Docker原理
  - KVM/QEMU
  - cgroup与namespace
- **实践**：手动实现一个简单容器

### 第12周：综合项目
- **实践项目**：
  - 搭建一个高可用Web服务
  - 实现自动扩容脚本
  - 编写系统优化报告

---

## 推荐资源

### 书籍
| 书名 | 难度 | 用途 |
|------|------|------|
| 《Linux命令行与shell脚本编程大全》 | 入门→进阶 | Shell |
| 《深入理解Linux内核》 | 高级 | 内核原理 |
| 《Linux高性能服务器编程》 | 进阶 | 系统编程 |
| 《Perf Recipes》 | 进阶 | 性能调优 |

### 在线教程
- [Linux Journey](https://linuxjourney.com/) - 免费入门
- [Linux Kernel Archives](https://www.kernel.org/) - 内核源码
- [Stack Overflow](https://stackoverflow.com/questions/tagged/linux) - 问题解答

### 实践环境
- [Play with Docker](https://labs.play-with-docker.com/) - 在线Docker练习
- [Linux Containers](https://linuxcontainers.org/) - 容器练习

---

## 每周时间建议

| 类别 | 时间 |
|------|------|
| 理论学习 | 3-4小时 |
| 实践操作 | 4-5小时 |
| 项目实战 | 2-3小时 |

---

## 快速上手命令

```bash
# 每天一条命令
# Week 1-2: sed, awk, grep
# Week 3-4: top, htop, strace
# Week 5-6: perf, vmstat
# Week 7-8: sysctl, tune2fs
```

---

**记住**：多动手、多踩坑是最好的学习方式！

有问题随时问我 🙌
