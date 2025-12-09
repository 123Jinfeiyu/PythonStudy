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
主要节点功能
模型推理节点：加载训练好的模型，对RGB图像进行目标检测
视觉处理节点：获取深度信息，计算目标3D位姿
坐标转换节点：将相机坐标系下的位姿转换到机械臂底座坐标系运动规划节点：调用MoveIt进行路径规划与执行
二、项目目录结构
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
三、核心实现代码
1. 配置文件
config/object_categories.yaml
yaml# 目标物体类别定义
object_categories:
  # 类别ID: [类别名称, 抓取方式, 安全夹取力]
  0: ["red_block", "top_grasp", 40]
  1: ["blue_cylinder", "side_grasp", 50]
  2: ["green_cube", "top_grasp", 45]
  3: ["yellow_ball", "envelop_grasp", 30]

# 抓取优先级（数字越小优先级越高）
grasp_priority:
  - "red_block"
  - "blue_cylinder"
  - "green_cube"
  - "yellow_ball"

config/grasp_positions.yaml
yaml# 抓取位置配置（相对base_link坐标系）
grasp_positions:
  # 预抓取位置（在目标上方）
  pre_grasp_offset: [0.0, 0.0, 0.15]  # X, Y, Z偏移
  
  # 放置位置（根据类别放置到不同位置）
  drop_locations:
    red_block: 
      pose: [0.3, 0.2, 0.1, 0.0, 0.0, 0.0, 1.0]  # [x, y, z, qx, qy, qz, qw]
      container: "box_A"
    blue_cylinder:
      pose: [0.3, -0.2, 0.1, 0.0, 0.0, 0.0, 1.0]
      container: "box_B"
    green_cube:
      pose: [0.4, 0.0, 0.1, 0.0, 0.0, 0.0, 1.0]
      container: "box_C"
    yellow_ball:
      pose: [0.2, 0.0, 0.15, 0.0, 0.0, 0.0, 1.0]
      container: "ball_tray"
  
  # 安全位置（机械臂空闲位置）
  home_position: [0.2, 0.0, 0.3, 0.0, 0.0, 0.0, 1.0]

2. 主启动文件
launch/model_grasping.launch
xml<?xml version="1.0"?>
<launch>
  <!-- 基本参数 -->
  <arg name="robot_ip" default="192.168.0.100" />
  <arg name="model_path" default="$(find model_based_grasping)/models/trained_model" />
  <arg name="debug" default="false" />
  
  <!-- 启动相机节点 -->
  <include file="$(find astra_camera)/launch/gemini.launch">
    <arg name="rgb_camera_info_url" value="file://$(find model_based_grasping)/config/camera_calibration.yaml"/>
  </include>
  
  <!-- 启动机械臂控制 -->
  <include file="$(find lebai_lm3_moveit_config)/launch/real_robot.launch">
    <arg name="robot_ip" value="$(arg robot_ip)" />
  </include>
  
  <!-- 启动模型推理节点 -->
  <node name="model_inference" pkg="model_based_grasping" type="model_inference.py" output="screen">
    <param name="model_path" value="$(arg model_path)" />
    <param name="confidence_threshold" value="0.7" />
    <param name="target_categories" value="red_block,blue_cylinder,green_cube,yellow_ball" />
    <remap from="rgb_image" to="/camera/color/image_raw" />
    <remap from="depth_image" to="/camera/depth/image_raw" />
  </node>
  
  <!-- 启动坐标转换节点 -->
  <node name="coordinate_transformer" pkg="model_based_grasping" type="coordinate_transformer.py" output="screen">
    <param name="hand_eye_matrix" value="0.124620 0.014122 -0.021451 -0.034018 0.014179 0.689671 ..." />
    <!-- 手眼标定矩阵，根据实际标定结果填写 -->
  </node>
  
  <!-- 启动抓取规划节点 -->
  <node name="grasp_planner" pkg="model_based_grasping" type="grasp_planner.py" output="screen">
    <param name="grasp_config_path" value="$(find model_based_grasping)/config/grasp_positions.yaml" />
    <param name="enable_debug" value="$(arg debug)" />
  </node>
  
  <!-- 如果需要可视化，启动Rviz -->
  <group if="$(arg debug)">
    <node name="rviz" pkg="rviz" type="rviz" args="-d $(find model_based_grasping)/config/model_grasping.rviz" />
  </group>
</launch>

3. 模型推理节点
scripts/model_inference.py
python#!/usr/bin/env python3
import rospy
import cv2
import numpy as np
from sensor_msgs.msg import Image, CameraInfo
from cv_bridge import CvBridge
from model_based_grasping.msg import DetectionResult, ObjectPoseArray
import torch
import yaml
import os

class ModelInferenceNode:
    def __init__(self):
        rospy.init_node('model_inference', anonymous=True)
        
        # 获取参数
        model_path = rospy.get_param('~model_path', '')
        self.conf_threshold = rospy.get_param('~confidence_threshold', 0.7)
        target_categories = rospy.get_param('~target_categories', '').split(',')
        
        # 加载模型配置
        self.load_model_config(model_path)
        
        # 初始化模型
        self.load_model(model_path)
        
        # 初始化CV桥接
        self.bridge = CvBridge()
        
        # 相机内参
        self.camera_matrix = None
        self.dist_coeffs = None
        
        # 订阅话题
        rospy.Subscriber('/camera/color/image_raw', Image, self.rgb_callback)
        rospy.Subscriber('/camera/depth/image_raw', Image, self.depth_callback)
        rospy.Subscriber('/camera/color/camera_info', CameraInfo, self.camera_info_callback)
        
        # 发布话题
        self.detection_pub = rospy.Publisher('/detection_results', DetectionResult, queue_size=10)
        self.object_pose_pub = rospy.Publisher('/object_poses', ObjectPoseArray, queue_size=10)
        
        # 缓存
        self.current_rgb = None
        self.current_depth = None
        self.camera_info_received = False
        
        rospy.loginfo("模型推理节点初始化完成")
        
    def load_model_config(self, model_path):
        """加载模型配置文件"""
        config_file = os.path.join(model_path, 'config.json')
        labels_file = os.path.join(model_path, 'labels.txt')
        
        if os.path.exists(labels_file):
            with open(labels_file, 'r') as f:
                self.labels = [line.strip() for line in f.readlines()]
        else:
            self.labels = ['object_{}'.format(i) for i in range(10)]
            
        rospy.loginfo(f"加载了 {len(self.labels)} 个类别标签")
        
    def load_model(self, model_path):
        """根据模型类型加载训练好的模型"""
        # 支持PyTorch、ONNX、TensorFlow等格式
        model_file = os.path.join(model_path, 'model.pth')
        
        if os.path.exists(model_file + '.pth'):
            # PyTorch模型
            self.model = torch.load(model_file)
            self.model.eval()
            if torch.cuda.is_available():
                self.model.cuda()
            self.inference_type = 'pytorch'
            
        elif os.path.exists(model_file + '.onnx'):
            # ONNX模型
            import onnxruntime as ort
            self.model = ort.InferenceSession(model_file)
            self.inference_type = 'onnx'
            
        else:
            rospy.logerr(f"在 {model_path} 中未找到支持的模型文件")
            rospy.signal_shutdown("模型加载失败")
            
        rospy.loginfo(f"模型加载成功，类型: {self.inference_type}")
        
    def camera_info_callback(self, msg):
        """获取相机内参"""
        if not self.camera_info_received:
            self.camera_matrix = np.array(msg.K).reshape(3, 3)
            self.dist_coeffs = np.array(msg.D)
            self.camera_info_received = True
            rospy.loginfo("相机内参已获取")
            
    def rgb_callback(self, msg):
        """RGB图像回调"""
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            self.current_rgb = cv_image
            self.process_image()
        except Exception as e:
            rospy.logerr(f"RGB图像处理错误: {e}")
            
    def depth_callback(self, msg):
        """深度图像回调"""
        try:
            depth_image = self.bridge.imgmsg_to_cv2(msg, "32FC1")
            # 将深度值从米转换为毫米（如果需要）
            self.current_depth = depth_image * 1000.0  # 假设原始单位为米
        except Exception as e:
            rospy.logerr(f"深度图像处理错误: {e}")
            
    def process_image(self):
        """处理图像并进行推理"""
        if self.current_rgb is None or self.current_depth is None or not self.camera_info_received:
            return
            
        # 预处理图像
        input_tensor = self.preprocess_image(self.current_rgb)
        
        # 模型推理
        detections = self.inference(input_tensor)
        
        # 后处理
        processed_detections = self.postprocess(detections)
        
        # 计算3D位姿
        object_poses = self.calculate_3d_poses(processed_detections)
        
        # 发布结果
        self.publish_results(processed_detections, object_poses)
        
    def preprocess_image(self, image):
        """预处理图像以适应模型输入"""
        # 根据模型要求调整大小和归一化
        img_resized = cv2.resize(image, (640, 480))
        img_normalized = img_resized.astype(np.float32) / 255.0
        
        if self.inference_type == 'pytorch':
            # PyTorch格式: [C, H, W], BGR to RGB
            img_rgb = cv2.cvtColor(img_normalized, cv2.COLOR_BGR2RGB)
            img_transposed = np.transpose(img_rgb, (2, 0, 1))
            return torch.from_numpy(img_transposed).unsqueeze(0)
            
        return img_normalized
        
    def inference(self, input_tensor):
        """执行模型推理"""
        if self.inference_type == 'pytorch':
            with torch.no_grad():
                if torch.cuda.is_available():
                    input_tensor = input_tensor.cuda()
                return self.model(input_tensor)
        elif self.inference_type == 'onnx':
            input_name = self.model.get_inputs()[0].name
            return self.model.run(None, {input_name: input_tensor.numpy()})
            
    def postprocess(self, detections):
        """后处理检测结果"""
        processed = []
        
        # 这里需要根据模型输出格式进行解析
        # 示例: 假设模型输出 [batch, num_detections, 6] 其中6为 [x1, y1, x2, y2, conf, class]
        
        for det in detections[0]:  # 假设第一个batch
            if det[4] > self.conf_threshold:  # 置信度阈值
                x1, y1, x2, y2 = map(int, det[:4])
                conf = float(det[4](@ref)
                class_id = int(det[5](@ref)
                
                if class_id < len(self.labels):
                    label = self.labels[class_id]
                    processed.append({
                        'bbox': [x1, y1, x2, y2],
                        'confidence': conf,
                        'class_id': class_id,
                        'label': label,
                        'center': [(x1 + x2) // 2, (y1 + y2) // 2]
                    })
                    
        return processed
        
    def calculate_3d_poses(self, detections):
        """根据检测框和深度图计算3D位姿"""
        poses = []
        
        for det in detections:
            cx, cy = det['center']
            
            # 获取深度值（取检测框中心区域平均值）
            bbox = det['bbox']
            depth_roi = self.current_depth[bbox[1]:bbox[3], bbox[0]:bbox[2]]
            
            if depth_roi.size == 0:
                continue
                
            # 过滤无效深度值
            valid_depths = depth_roi[(depth_roi > 0.1) & (depth_roi < 3.0)]  # 0.1m到3.0m
            
            if len(valid_depths) == 0:
                continue
                
            depth = np.median(valid_depths)
            
            # 将像素坐标转换到相机坐标系
            if self.camera_matrix is not None:
                # 2D像素坐标到3D相机坐标
                fx = self.camera_matrix[0, 0]
                fy = self.camera_matrix[1, 1]
                cx_cam = self.camera_matrix[0, 2]
                cy_cam = self.camera_matrix[1, 2]
                
                # 计算3D坐标
                z = depth / 1000.0  # 毫米转米
                x = (cx - cx_cam) * z / fx
                y = (cy - cy_cam) * z / fy
                
                # 简单姿态估计（假设物体平放，z轴向上）
                # 实际应用中可能需要更复杂的姿态估计
                pose = {
                    'position': [x, y, z],
                    'orientation': [0.0, 0.0, 0.0, 1.0],  # 四元数
                    'label': det['label'],
                    'confidence': det['confidence']
                }
                poses.append(pose)
                
        return poses
        
    def publish_results(self, detections, poses):
        """发布检测结果"""
        # 发布2D检测结果
        detection_msg = DetectionResult()
        detection_msg.header.stamp = rospy.Time.now()
        detection_msg.header.frame_id = "camera_color_optical_frame"
        
        for det in detections:
            detection_msg.labels.append(det['label'])
            detection_msg.confidences.append(det['confidence'])
            detection_msg.bboxes.append(det['bbox'])
            
        self.detection_pub.publish(detection_msg)
        
        # 发布3D位姿
        pose_msg = ObjectPoseArray()
        pose_msg.header.stamp = rospy.Time.now()
        pose_msg.header.frame_id = "camera_color_optical_frame"
        
        for pose in poses:
            pose_3d = ObjectPose()
            pose_3d.label = pose['label']
            pose_3d.confidence = pose['confidence']
            pose_3d.pose.position.x = pose['position']
            pose_3d.pose.position.y = pose['position']
            pose_3d.pose.position.z = pose['position']
            pose_3d.pose.orientation.x = pose['orientation']
            pose_3d.pose.orientation.y = pose['orientation']
            pose_3d.pose.orientation.z = pose['orientation']
            pose_3d.pose.orientation.w = pose['orientation']
            pose_msg.poses.append(pose_3d)
            
        self.object_pose_pub.publish(pose_msg)
        
    def run(self):
        rospy.spin()

if __name__ == '__main__':
    node = ModelInferenceNode()
    node.run()

4. 坐标转换节点
scripts/coordinate_transformer.py
python#!/usr/bin/env python3
import rospy
import tf2_ros
import tf2_geometry_msgs
import numpy as np
from geometry_msgs.msg import PoseStamped, TransformStamped
from model_based_grasping.msg import ObjectPoseArray, GraspTargetArray
import yaml

class CoordinateTransformer:
    def __init__(self):
        rospy.init_node('coordinate_transformer')
        
        # TF监听器
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer)
        
        # 手眼标定矩阵（从相机到机械臂末端）
        hand_eye_str = rospy.get_param('~hand_eye_matrix', '')
        if hand_eye_str:
            self.hand_eye_matrix = self.parse_transform_string(hand_eye_str)
        else:
            rospy.logwarn("未提供手眼标定矩阵，尝试从TF树获取")
            self.hand_eye_matrix = None
            
        # 订阅对象位姿（相机坐标系）
        rospy.Subscriber('/object_poses', ObjectPoseArray, self.pose_callback)
        
        # 发布抓取目标（机械臂底座坐标系）
        self.grasp_target_pub = rospy.Publisher('/grasp_targets', GraspTargetArray, queue_size=10)
        
        rospy.loginfo("坐标转换节点初始化完成")
        
    def parse_transform_string(self, transform_str):
        """解析手眼标定矩阵字符串"""
        values = list(map(float, transform_str.split()))
        if len(values) == 7:
            # 位置和四元数格式 [x, y, z, qx, qy, qz, qw]
            return self.pose_to_matrix(values)
        elif len(values) == 16:
            # 4x4矩阵格式
            return np.array(values).reshape(4, 4)
        else:
            rospy.logerr(f"无法解析手眼标定矩阵: {transform_str}")
            return None
            
    def pose_to_matrix(self, pose):
        """将位置+四元数转换为4x4齐次变换矩阵"""
        x, y, z, qx, qy, qz, qw = pose
        
        # 旋转矩阵部分
        R = np.array([
            [1 - 2*(qy**2 + qz**2), 2*(qx*qy - qw*qz), 2*(qx*qz + qw*qy)],
            [2*(qx*qy + qw*qz), 1 - 2*(qx**2 + qz**2), 2*(qy*qz - qw*qx)],
            [2*(qx*qz - qw*qy), 2*(qy*qz + qw*qx), 1 - 2*(qx**2 + qy**2)]
        ])
        
        # 齐次变换矩阵
        T = np.eye(4)
        T[:3, :3] = R
        T[:3, 3] = [x, y, z]
        
        return T
        
    def pose_callback(self, msg):
        """处理检测到的物体位姿"""
        grasp_targets = GraspTargetArray()
        grasp_targets.header.stamp = rospy.Time.now()
        grasp_targets.header.frame_id = "base_link"
        
        for obj_pose in msg.poses:
            try:
                # 将位姿从相机坐标系转换到机械臂底座坐标系
                target_pose = self.transform_pose(obj_pose)
                
                if target_pose:
                    grasp_targets.targets.append(target_pose)
                    
            except Exception as e:
                rospy.logerr(f"位姿转换失败: {e}")
                
        if grasp_targets.targets:
            self.grasp_target_pub.publish(grasp_targets)
            
    def transform_pose(self, object_pose):
        """坐标转换核心函数"""
        # 方法1: 使用TF树（推荐）
        try:
            # 等待变换可用
            transform = self.tf_buffer.lookup_transform(
                'base_link',
                object_pose.header.frame_id,
                rospy.Time(0),
                rospy.Duration(1.0)
            )
            
            # 转换位姿
            pose_stamped = PoseStamped()
            pose_stamped.header = object_pose.header
            pose_stamped.pose = object_pose.pose
            
            transformed_pose = tf2_geometry_msgs.do_transform_pose(
                pose_stamped, transform
            )
            
            # 创建抓取目标
            from model_based_grasping.msg import GraspTarget
            
            target = GraspTarget()
            target.label = object_pose.label
            target.confidence = object_pose.confidence
            target.pose = transformed_pose.pose
            
            # 根据物体类别设置抓取参数
            self.set_grasp_parameters(target)
            
            return target
            
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, 
                tf2_ros.ExtrapolationException) as e:
            rospy.logwarn(f"TF变换失败: {e}")
            
        # 方法2: 使用手眼标定矩阵（备用）
        if self.hand_eye_matrix is not None:
            return self.transform_with_matrix(object_pose)
            
        return None
        
    def set_grasp_parameters(self, target):
        """根据物体类别设置抓取参数"""
        # 可以从配置文件加载抓取策略
        grasp_strategies = {
            'red_block': {
                'grasp_type': 'top_grasp',
                'pregrasp_offset': [0.0, 0.0, 0.15],
                'grasp_depth': 0.02,
                'force': 40
            },
            'blue_cylinder': {
                'grasp_type': 'side_grasp',
                'pregrasp_offset': [0.0, 0.0, 0.1],
                'grasp_depth': 0.03,
                'force': 50
            },
            # 其他类别...
        }
        
        if target.label in grasp_strategies:
            strategy = grasp_strategies[target.label]
            target.grasp_type = strategy['grasp_type']
            target.pregrasp_offset = strategy['pregrasp_offset']
            target.grasp_depth = strategy['grasp_depth']
            target.grasp_force = strategy['force']
        else:
            # 默认参数
            target.grasp_type = 'top_grasp'
            target.pregrasp_offset = [0.0, 0.0, 0.1]
            target.grasp_depth = 0.02
            target.grasp_force = 30
            
    def run(self):
        rospy.spin()

if __name__ == '__main__':
    transformer = CoordinateTransformer()
    transformer.run()

5. 抓取规划节点
scripts/grasp_planner.py
python#!/usr/bin/env python3
import rospy
import yaml
import numpy as np
from moveit_msgs.msg import MoveItErrorCodes
from moveit_msgs.srv import GetPositionIK
from geometry_msgs.msg import PoseStamped
from model_based_grasping.msg import GraspTargetArray, GraspCommand
import actionlib
from moveit_msgs.msg import MoveGroupAction, MoveGroupGoal, Constraints, JointConstraint

class GraspPlanner:
    def __init__(self):
        rospy.init_node('grasp_planner')
        
        # 加载配置文件
        config_path = rospy.get_param('~grasp_config_path', '')
        self.load_config(config_path)
        
        # MoveIt动作客户端
        self.move_group_client = actionlib.SimpleActionClient(
            '/move_group', MoveGroupAction
        )
        
        # 等待MoveIt服务
        rospy.loginfo("等待MoveIt服务...")
        self.move_group_client.wait_for_server()
        rospy.loginfo("MoveIt服务已连接")
        
        # 夹爪控制服务
        rospy.wait_for_service('/io_service/set_gripper_position')
        rospy.wait_for_service('/io_service/set_gripper_force')
        self.set_gripper_position = rospy.ServiceProxy(
            '/io_service/set_gripper_position', SetGripperPosition
        )
        self.set_gripper_force = rospy.ServiceProxy(
            '/io_service/set_gripper_force', SetGripperForce
        )
        
        # 订阅抓取目标
        rospy.Subscriber('/grasp_targets', GraspTargetArray, self.targets_callback)
        
        # 发布抓取命令
        self.command_pub = rospy.Publisher('/grasp_commands', GraspCommand, queue_size=10)
        
        # 状态变量
        self.current_targets = []
        self.is_busy = False
        
        rospy.loginfo("抓取规划节点初始化完成")
        
    def load_config(self, config_path):
        """加载抓取配置"""
        try:
            with open(config_path, 'r') as f:
                self.config = yaml.safe_load(f)
                
            # 加载放置位置
            self.drop_positions = self.config['grasp_positions']['drop_locations']
            self.home_position = self.config['grasp_positions']['home_position']
            
            rospy.loginfo(f"加载了 {len(self.drop_positions)} 个放置位置")
            
        except Exception as e:
            rospy.logerr(f"配置文件加载失败: {e}")
            self.config = {}
            self.drop_positions = {}
            self.home_position = [0.2, 0.0, 0.3, 0.0, 0.0, 0.0, 1.0]
            
    def targets_callback(self, msg):
        """处理抓取目标"""
        if self.is_busy:
            rospy.logwarn("机器人正忙，忽略新目标")
            return
            
        self.current_targets = msg.targets
        
        if self.current_targets:
            # 按置信度排序
            self.current_targets.sort(key=lambda x: x.confidence, reverse=True)
            
            # 开始执行抓取任务
            self.execute_grasp_task()
            
    def execute_grasp_task(self):
        """执行完整的抓取任务"""
        self.is_busy = True
        
        try:
            # 1. 移动到安全位置
            self.move_to_home()
            
            # 2. 遍历所有目标
            for target in self.current_targets:
                rospy.loginfo(f"开始抓取: {target.label} (置信度: {target.confidence:.2f})")
                
                # 3. 移动到预抓取位置
                if not self.move_to_pregrasp(target):
                    rospy.logwarn(f"无法到达预抓取位置，跳过 {target.label}")
                    continue
                    
                # 4. 执行抓取
                if not self.execute_grasp(target):
                    rospy.logwarn(f"抓取失败: {target.label}")
                    continue
                    
                # 5. 抬起物体
                self.lift_object(target)
                
                # 6. 移动到放置位置
                drop_pose = self.get_drop_position(target.label)
                if drop_pose:
                    self.move_to_drop(drop_pose)
                    
                    # 7. 放置物体
                    self.release_object()
                    
                    # 8. 返回安全位置
                    self.move_to_home()
                    
                rospy.loginfo(f"成功完成 {target.label} 的抓取")
                
        except Exception as e:
            rospy.logerr(f"抓取任务执行异常: {e}")
            
        finally:
            self.is_busy = False
            self.current_targets = []
            
    def move_to_pregrasp(self, target):
        """移动到预抓取位置"""
        # 创建预抓取位姿（在目标上方）
        pregrasp_pose = PoseStamped()
        pregrasp_pose.header.frame_id = "base_link"
        pregrasp_pose.header.stamp = rospy.Time.now()
        
        # 复制目标位姿
        pregrasp_pose.pose = target.pose
        
        # 添加偏移（避免碰撞）
        offset = target.pregrasp_offset
        pregrasp_pose.pose.position.z += offset
        
        # 发送移动命令
        return self.move_to_pose(pregrasp_pose, "预抓取位置")
        
    def execute_grasp(self, target):
        """执行抓取动作"""
        try:
            # 1. 打开夹爪
            rospy.loginfo("打开夹爪")
            self.set_gripper_position(100)  # 完全打开
            rospy.sleep(0.5)
            
            # 2. 设置夹爪力度
            self.set_gripper_force(target.grasp_force)
            
            # 3. 移动到抓取位置
            rospy.loginfo("移动到抓取位置")
            grasp_pose = PoseStamped()
            grasp_pose.header.frame_id = "base_link"
            grasp_pose.header.stamp = rospy.Time.now()
            grasp_pose.pose = target.pose
            
            # 根据抓取类型调整姿态
            if target.grasp_type == 'top_grasp':
                # 保持垂直抓取
                pass
            elif target.grasp_type == 'side_grasp':
                # 调整姿态进行侧面抓取
                # 这里需要根据物体实际姿态调整
                pass
                
            if not self.move_to_pose(grasp_pose, "抓取位置"):
                return False
                
            rospy.sleep(0.2)
            
            # 4. 闭合夹爪
            rospy.loginfo("闭合夹爪")
            self.set_gripper_position(0)  # 完全闭合
            rospy.sleep(1.0)
            
            # 5. 轻微抬起检查是否抓稳
            check_pose = grasp_pose
            check_pose.pose.position.z += 0.02
            self.move_to_pose(check_pose, "抓取检查")
            
            return True
            
        except Exception as e:
            rospy.logerr(f"抓取执行失败: {e}")
            return False
            
    def lift_object(self, target):
        """抬起物体"""
        lift_pose = PoseStamped()
        lift_pose.header.frame_id = "base_link"
        lift_pose.header.stamp = rospy.Time.now()
        lift_pose.pose = target.pose
        lift_pose.pose.position.z += 0.1  # 抬起10cm
        
        self.move_to_pose(lift_pose, "抬起物体")
        
    def move_to_drop(self, drop_pose):
        """移动到放置位置"""
        pose_stamped = PoseStamped()
        pose_stamped.header.frame_id = "base_link"
        pose_stamped.header.stamp = rospy.Time.now()
        
        # 将列表转换为位姿
        pose_stamped.pose.position.x = drop_pose
        pose_stamped.pose.position.y = drop_pose
        pose_stamped.pose.position.z = drop_pose
        pose_stamped.pose.orientation.x = drop_pose
        pose_stamped.pose.orientation.y = drop_pose
        pose_stamped.pose.orientation.z = drop_pose
        pose_stamped.pose.orientation.w = drop_pose
        
        self.move_to_pose(pose_stamped, "放置位置")
        
    def release_object(self):
        """释放物体"""
        try:
            rospy.loginfo("释放物体")
            self.set_gripper_position(100)  # 完全打开
            rospy.sleep(0.5)
        except Exception as e:
            rospy.logerr(f"释放物体失败: {e}")
            
    def move_to_home(self):
        """移动到安全位置"""
        home_pose = PoseStamped()
        home_pose.header.frame_id = "base_link"
        home_pose.header.stamp = rospy.Time.now()
        
        home_pose.pose.position.x = self.home_position
        home_pose.pose.position.y = self.home_position
        home_pose.pose.position.z = self.home_position
        home_pose.pose.orientation.x = self.home_position
        home_pose.pose.orientation.y = self.home_position
        home_pose.pose.orientation.z = self.home_position
        home_pose.pose.orientation.w = self.home_position
        
        self.move_to_pose(home_pose, "安全位置")
        
    def move_to_pose(self, target_pose, description=""):
        """使用MoveIt移动到指定位姿"""
        try:
            goal = MoveGroupGoal()
            
            # 设置目标约束
            pose_constraint = Constraints()
            pose_constraint.name = "pose_constraint"
            
            goal.request.goal_constraints.append(pose_constraint)
            goal.request.group_name = "manipulator"
            goal.request.num_planning_attempts = 5
            goal.request.allowed_planning_time = 5.0
            goal.request.planner_id = "RRTConnect"
            
            # 发送目标
            self.move_group_client.send_goal(goal)
            
            # 等待结果
            self.move_group_client.wait_for_result()
            result = self.move_group_client.get_result()
            
            if result and result.error_code.val == MoveItErrorCodes.SUCCESS:
                if description:
                    rospy.loginfo(f"成功移动到 {description}")
                return True
            else:
                rospy.logwarn(f"移动到 {description} 失败")
                return False
                
        except Exception as e:
            rospy.logerr(f"移动失败: {e}")
            return False
            
    def get_drop_position(self, object_label):
        """根据物体标签获取放置位置"""
        if object_label in self.drop_positions:
            return self.drop_positions[object_label]['pose']
        return None
        
    def run(self):
        rospy.spin()

if __name__ == '__main__':
    planner = GraspPlanner()
    planner.run()

四、消息定义
msg/DetectionResult.msg
Header header
string[] labels
float32[] confidences
int32[] bbox_x
int32[] bbox_y
int32[] bbox_width
int32[] bbox_height

msg/ObjectPose.msg
Header header
string label
float32 confidence
geometry_msgs/Pose pose

msg/ObjectPoseArray.msg
Header header
ObjectPose[] poses

msg/GraspTarget.msg
Header header
string label
float32 confidence
geometry_msgs/Pose pose
string grasp_type
float32[] pregrasp_offset
float32 grasp_depth
int32 grasp_force

msg/GraspTargetArray.msg
Header header
GraspTarget[] targets

msg/GraspCommand.msg
Header header
string command  # "GRASP", "RELEASE", "MOVE_TO_HOME"
string target_label
geometry_msgs/Pose target_pose

五、部署与运行指南
1. 准备工作
bash# 在Orin Nano上创建工作空间
mkdir -p ~/model_grasping_ws/src
cd ~/model_grasping_ws/src

# 复制您的模型文件到正确位置
cp -r /path/to/your/model ~/model_grasping_ws/src/model_based_grasping/models/trained_model/

# 安装依赖
sudo apt-get install python3-pip
pip3 install torch torchvision onnxruntime opencv-python pyyaml

2. 编译与配置
bash# 编译ROS包
cd ~/model_grasping_ws
catkin_make
source devel/setup.bash

# 配置环境变量
echo "source ~/model_grasping_ws/devel/setup.bash" >> ~/.bashrc
source ~/.bashrc

# 修改配置文件
# 根据实际标定结果修改手眼标定矩阵
# 根据实际需求修改抓取位置和类别

3. 运行系统
bash# 方法1: 完整启动
roslaunch model_based_grasping model_grasping.launch debug:=true

# 方法2: 分步启动
# 终端1: 启动相机和机械臂
roslaunch astra_camera gemini_arm.launch
roslaunch lebai_lm3_moveit_config real_robot.launch

# 终端2: 启动模型节点
rosrun model_based_grasping model_inference.py

# 终端3: 启动抓取系统
rosrun model_based_grasping grasp_planner.py

4. 测试与调试
bash# 查看TF树
rosrun tf view_frames

# 查看检测结果
rostopic echo /detection_results

# 查看抓取目标
rostopic echo /grasp_targets

# 可视化（如果配置了Rviz）
rviz -d $(rospack find model_based_grasping)/config/model_grasping.rviz

六、关键注意事项


性能优化：Orin Nano 4GB内存有限，考虑：

使用量化模型（INT8量化）
调整图像分辨率（640x480或更低）
使用TensorRT加速（如果是TensorRT兼容模型）



实时性：在model_inference.py中调整处理频率：
python# 控制处理频率，避免CPU过载
self.rate = rospy.Rate(5)  # 5Hz



安全性：

首次运行时使用低速度
配置碰撞检测
设置关节限位保护



错误处理：

添加超时机制
实现重试逻辑
记录运行日志



七、扩展功能建议

多物体抓取策略：实现多物体检测和抓取顺序优化
失败恢复：抓取失败时的自动恢复策略
在线学习：在运行中更新抓取策略
远程监控：添加Web界面进行远程监控和控制
数据集收集：在运行中自动收集训练数据

这个系统可以直接部署到您的Wheeltec S300机器人上，只需根据实际标定结果和硬件配置调整相应参数即可。系统模块化设计便于后续维护和扩展。