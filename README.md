# PythonStudy
This is a good project to study the popular language Programming Python

## 项目目录

### 1. wheeltec_robot - 基于模型的机械臂抓取系统

这是一个基于ROS的机械臂抓取系统，实现了从目标检测到抓取执行的完整流程。

#### 系统架构
```
┌─────────────────────────────────────────────────────────────┐
│                    ROS Master (Orin Nano)                   │
├─────────────────────────────────────────────────────────────┤
│ 模型推理节点  │  视觉处理节点  │  TF坐标转换  │  MoveIt控制  │
└─────────────────────────────────────────────────────────────┘
         │              │             │            │
         ▼              ▼             ▼            ▼
┌─────────────────────────────────────────────────────────────┐
│      深度相机      │   机械臂驱动   │    夹爪控制    │
└─────────────────────────────────────────────────────────────┘
```

#### 主要功能
- **模型推理节点**：加载训练好的模型，对RGB图像进行目标检测
- **视觉处理节点**：获取深度信息，计算目标3D位姿
- **坐标转换节点**：将相机坐标系下的位姿转换到机械臂底座坐标系
- **运动规划节点**：调用MoveIt进行路径规划与执行

#### 目录结构
```
wheeltec_robot/
└── src/
    └── model_based_grasping/
        ├── CMakeLists.txt
        ├── package.xml
        ├── launch/
        │   ├── model_grasping.launch      # 主启动文件
        │   ├── camera.launch              # 相机启动
        │   └── robot_control.launch       # 机械臂控制
        ├── config/
        │   ├── object_categories.yaml     # 类别配置文件
        │   ├── grasp_positions.yaml       # 抓取位置配置
        │   └── model_params.yaml          # 模型参数配置
        ├── scripts/
        │   ├── model_inference.py         # 模型推理节点
        │   ├── grasp_planner.py           # 抓取规划节点
        │   └── coordinate_transformer.py  # 坐标转换节点
        ├── src/
        │   ├── model_grasping/
        │   │   ├── __init__.py
        │   │   ├── object_detector.py     # 目标检测类
        │   │   ├── pose_estimator.py      # 位姿估计类
        │   │   └── grasp_executor.py      # 抓取执行类
        │   └── utils/
        │       ├── tf_utils.py            # TF工具函数
        │       └── camera_utils.py        # 相机工具函数
        ├── msg/
        │   ├── DetectionResult.msg        # 检测结果消息
        │   ├── ObjectPose.msg             # 物体位姿消息
        │   ├── ObjectPoseArray.msg        # 物体位姿数组消息
        │   ├── GraspTarget.msg            # 抓取目标消息
        │   ├── GraspTargetArray.msg       # 抓取目标数组消息
        │   └── GraspCommand.msg           # 抓取命令消息
        └── models/
            └── trained_model/             # 训练好的模型文件
                ├── model.pth/.onnx/.pb
                ├── config.json
                └── labels.txt
```

#### 核心功能说明
1. **目标检测**：使用深度学习模型识别场景中的物体
2. **位姿估计**：基于深度相机数据计算物体的3D位姿
3. **抓取规划**：根据物体位姿和类别确定最佳抓取方式
4. **路径规划**：使用MoveIt规划机械臂运动路径
5. **抓取执行**：控制机械臂和夹爪完成抓取操作

#### 启动方式
```bash
roslaunch model_based_grasping model_grasping.launch
```

## 贡献
欢迎提交Issue和Pull Request来改进这个项目。

## 许可证
本项目采用MIT许可证。
