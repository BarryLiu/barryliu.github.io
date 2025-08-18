## 学习Rust



[官网地址](https://www.rust-lang.org/zh-CN/learn/get-started)

安装好查看版本

``` shell
rustc -V
```



* cargo 

### Cargo：Rust 的构建工具和包管理器

您在安装 Rustup 时，也会安装 Rust 构建工具和包管理器的最新稳定版，即 Cargo。Cargo 可以做很多事情：

- `cargo build` 可以构建项目
- `cargo run` 可以运行项目
- `cargo test` 可以测试项目
- `cargo doc` 可以为项目构建文档
- `cargo publish` 可以将库发布到 [crates.io](https://crates.io/)。

要检查您是否安装了 Rust 和 Cargo，可以在终端中运行：

```
cargo --version
```



#### 新建工程

* cargo new xxxx  --新建工程
* cargo init --初始化工程



#### rust官方仓库(https://crates.io/)

* 添加依赖

  > 命令 : cargo add ferris-says