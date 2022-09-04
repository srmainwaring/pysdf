from __future__ import print_function

import numbers
import numpy as np

from geometry_msgs.msg import Pose

# from tf.transformations import *

from transforms3d import affines
from transforms3d import euler
from transforms3d import quaternions

def translation_from_matrix(matrix):
  T, R, Z, S = affines.decompose(matrix)
  return T

def quaternion_from_matrix(matrix):
  T, R, Z, S = affines.decompose(matrix)
  return quaternions.mat2quat(R)

def euler_from_matrix(matrix, axes='sxyz'):
  T, R, Z, S = affines.decompose(matrix)
  return euler.mat2euler(R, axes=axes)

def translation_matrix(direction):
  T = direction
  R = np.identity(3)
  Z = np.ones((3))
  H = affines.compose(T, R, Z)
  return H

def quaternion_matrix(q):
  T = np.zeros((3))
  R = quaternions.quat2mat(q)
  Z = np.ones((3))
  H = affines.compose(T, R, Z)
  return H

def concatenate_matrices(*matrices):
  M = matrices[0]
  for x in matrices[1:]:
    M = np.matmul(M, x)
  return M

def euler_matrix(ai, aj, ak, axes='sxyz'):
  T = np.zeros((3))
  R = euler.euler2mat(ai, aj, ak, axes)
  Z = np.ones((3))
  H = affines.compose(T, R, Z)
  return H

def compose_matrix(scale=None, shear=None, angles=None, translate=None, perspective=None):
  T = translate
  R = euler.euler2mat(angles, axes='sxyz')
  Z = np.ones((3))
  H = affines.compose(T, R, Z)
  return H

# from tf.transformations import *


def rounded(val):
  if isinstance(val, str):
    return rounded(float(val))
  elif isinstance(val, numbers.Number):
    return int(round(val,6) * 1e5) / 1.0e5
  else:
    return np.array([rounded(v) for v in val])


def homogeneous2translation_quaternion(homogeneous):
  """
  Translation: [x, y, z]
  Quaternion: [x, y, z, w]
  """
  translation = translation_from_matrix(homogeneous)
  quaternion = quaternion_from_matrix(homogeneous)
  return translation, quaternion


def homogeneous2translation_rpy(homogeneous):
  """
  Translation: [x, y, z]
  RPY: [sx, sy, sz]
  """
  translation = translation_from_matrix(homogeneous)
  rpy = euler_from_matrix(homogeneous)
  return translation, rpy


def homogeneous2pose_msg(homogeneous):
  pose = Pose()
  translation, quaternion = homogeneous2translation_quaternion(homogeneous)
  pose.position.x = translation[0]
  pose.position.y = translation[1]
  pose.position.z = translation[2]
  pose.orientation.x = quaternion[0]
  pose.orientation.y = quaternion[1]
  pose.orientation.z = quaternion[2]
  pose.orientation.w = quaternion[3]
  return pose


def pose_msg2homogeneous(pose):
  trans = translation_matrix((pose.position.x, pose.position.y, pose.position.z))
  rot = quaternion_matrix((pose.orientation.x, pose.orientation.y, pose.orientation.z, pose.orientation.w))
  return concatenate_matrices(trans, rot)


def array2string(array):
  return np.array_str(array).strip('[]. ').replace('. ', ' ')


def homogeneous2tq_string(homogeneous):
  return 't=%s q=%s' % homogeneous2translation_quaternion(homogeneous)


def homogeneous2tq_string_rounded(homogeneous):
  return 't=%s q=%s' % tuple(rounded(o) for o in homogeneous2translation_quaternion(homogeneous))


def string2float_list(s):
  return [float(i) for i in s.split()]


def pose_string2homogeneous(pose):
  pose_float = string2float_list(pose)
  translate = pose_float[:3]
  angles = pose_float[3:]
  homogeneous = compose_matrix(None, None, angles, translate)
  #print('pose_string=%s; translate=%s angles=%s homogeneous:\n%s' % (pose, translate, angles, homogeneous))
  return homogeneous


def rotation_only(homogeneous):
  euler = euler_from_matrix(homogeneous)
  return euler_matrix(euler[0], euler[1], euler[2])
