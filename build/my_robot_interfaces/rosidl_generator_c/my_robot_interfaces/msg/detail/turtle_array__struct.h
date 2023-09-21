// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from my_robot_interfaces:msg/TurtleArray.idl
// generated code does not contain a copyright notice

#ifndef MY_ROBOT_INTERFACES__MSG__DETAIL__TURTLE_ARRAY__STRUCT_H_
#define MY_ROBOT_INTERFACES__MSG__DETAIL__TURTLE_ARRAY__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'alive_turtles'
#include "rosidl_runtime_c/string.h"

// constants for array fields with an upper bound
// alive_turtles
enum
{
  my_robot_interfaces__msg__TurtleArray__alive_turtles__MAX_STRING_SIZE = 100
};

// Struct defined in msg/TurtleArray in the package my_robot_interfaces.
typedef struct my_robot_interfaces__msg__TurtleArray
{
  rosidl_runtime_c__String__Sequence alive_turtles;
} my_robot_interfaces__msg__TurtleArray;

// Struct for a sequence of my_robot_interfaces__msg__TurtleArray.
typedef struct my_robot_interfaces__msg__TurtleArray__Sequence
{
  my_robot_interfaces__msg__TurtleArray * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} my_robot_interfaces__msg__TurtleArray__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // MY_ROBOT_INTERFACES__MSG__DETAIL__TURTLE_ARRAY__STRUCT_H_
