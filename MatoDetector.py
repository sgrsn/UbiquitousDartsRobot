#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file MatoDetector.py
 @brief Mato Detection Component
 @date $Date$


"""
import sys
import time
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist

import cv2
import numpy as np


# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
matodetector_spec = ["implementation_id", "MatoDetector",
     "type_name",         "MatoDetector",
     "description",       "Mato Detection Component",
     "version",           "1.0.0",
     "vendor",            "Hidaka Sato",
     "category",          "ImageProcessiong",
     "activity_type",     "STATIC",
     "max_instance",      "1",
     "language",          "Python",
     "lang_type",         "SCRIPT",
     "conf.default.param1", "100",
     "conf.default.param2", "40",
     "conf.default.max_radius", "300",
     "conf.default.min_radius", "30",
     "conf.default.camera_port", "0",
     "conf.default.dp", "20",

     "conf.__widget__.param1", "slider.1",
     "conf.__widget__.param2", "slider.1",
     "conf.__widget__.max_radius", "slider.1",
     "conf.__widget__.min_radius", "spin.1",
     "conf.__widget__.camera_port", "radio",
     "conf.__widget__.dp", "slider.1",
     "conf.__constraints__.param1", "0<x<200",
     "conf.__constraints__.param2", "0<x<200",
     "conf.__constraints__.max_radius", "0<x<1000",
     "conf.__constraints__.min_radius", "0<x<1000",
     "conf.__constraints__.camera_port", "(0,1,2,3,4)",
     "conf.__constraints__.dp", "0<x<100",

         "conf.__type__.param1", "int",
         "conf.__type__.param2", "int",
         "conf.__type__.max_radius", "int",
         "conf.__type__.min_radius", "int",
         "conf.__type__.camera_port", "int",
         "conf.__type__.dp", "int",

     ""]
# </rtc-template>

##
# @class MatoDetector
# @brief Mato Detection Component
#
#
class MatoDetector(OpenRTM_aist.DataFlowComponentBase):

  ##
  # @brief constructor
  # @param manager Maneger Object
  #
  def __init__(self, manager):
    OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

    self._d_target_output = OpenRTM_aist.instantiateDataType(RTC.TimedPose2D)
    """
    """
    self._target_outputOut = OpenRTM_aist.OutPort("target_output", self._d_target_output)





    # initialize of configuration-data.
    # <rtc-template block="init_conf_param">
    """
    
     - Name:  param1
     - DefaultValue: 100
    """
    self._param1 = [100]
    """
    
     - Name:  param2
     - DefaultValue: 40
    """
    self._param2 = [40]
    """
    
     - Name:  max_radius
     - DefaultValue: 300
    """
    self._max_radius = [300]
    """
    
     - Name:  min_radius
     - DefaultValue: 30
    """
    self._min_radius = [30]
    """
    
     - Name:  camera_port
     - DefaultValue: 0
    """
    self._camera_port = [0]
    """
    
     - Name:  dp
     - DefaultValue: 20
    """
    self._dp = [20]

    # </rtc-template>



  ##
  #
  # The initialize action (on CREATED->ALIVE transition)
  # formaer rtc_init_entry()
  #
  # @return RTC::ReturnCode_t
  #
  #
  def onInitialize(self):
    # Bind variables and configuration variable
    self.bindParameter("param1", self._param1, "100")
    self.bindParameter("param2", self._param2, "40")
    self.bindParameter("max_radius", self._max_radius, "300")
    self.bindParameter("min_radius", self._min_radius, "30")
    self.bindParameter("camera_port", self._camera_port, "0")
    self.bindParameter("dp", self._dp, "20")

    # Set InPort buffers

    # Set OutPort buffers
    self.addOutPort("target_output",self._target_outputOut)

    # Set service provider to Ports

    # Set service consumers to Ports

    # Set CORBA Service Ports
    
    return RTC.RTC_OK

  ###
  ##
  ## The finalize action (on ALIVE->END transition)
  ## formaer rtc_exiting_entry()
  ##
  ## @return RTC::ReturnCode_t
  #
  ##
  #def onFinalize(self):
  #
  #  return RTC.RTC_OK

  ###
  ##
  ## The startup action when ExecutionContext startup
  ## former rtc_starting_entry()
  ##
  ## @param ec_id target ExecutionContext Id
  ##
  ## @return RTC::ReturnCode_t
  ##
  ##
  #def onStartup(self, ec_id):
  #
  #  return RTC.RTC_OK

  ###
  ##
  ## The shutdown action when ExecutionContext stop
  ## former rtc_stopping_entry()
  ##
  ## @param ec_id target ExecutionContext Id
  ##
  ## @return RTC::ReturnCode_t
  ##
  ##
  #def onShutdown(self, ec_id):
  #
  #  return RTC.RTC_OK

  ##
  #
  # The activated action (Active state entry action)
  # former rtc_active_entry()
  #
  # @param ec_id target ExecutionContext Id
  #
  # @return RTC::ReturnCode_t
  #
  #
  def onActivated(self, ec_id):
    self.capture = cv2.VideoCapture(int(self._camera_port[0]))
    ret, img = self.capture.read()
    self.height = img.shape[0]
    self.width = img.shape[1]
    return RTC.RTC_OK

  ##
  #
  # The deactivated action (Active state exit action)
  # former rtc_active_exit()
  #
  # @param ec_id target ExecutionContext Id
  #
  # @return RTC::ReturnCode_t
  #
  #
  def onDeactivated(self, ec_id):
    cv2.destroyAllWindows()
    return RTC.RTC_OK

  ##
  #
  # The execution action that is invoked periodically
  # former rtc_active_do()
  #
  # @param ec_id target ExecutionContext Id
  #
  # @return RTC::ReturnCode_t
  #
  #
  def onExecute(self, ec_id):
    ret, img = self.capture.read()
    img = cv2.medianBlur(img,5)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    circles = cv2.HoughCircles(
      gray,
      cv2.HOUGH_GRADIENT,
      1,
      int(self._dp[0]),
      param1=int(self._param1[0]),
      param2=int(self._param2[0]),
      minRadius=int(self._min_radius[0]),
      maxRadius=int(self._max_radius[0])
    )
    if circles is not None:
      circles = np.uint16(np.around(circles))
      mato_point = np.mean(circles[0,:], axis=0)
      self._d_target_output.data.position.x = float(mato_point[0]) - self.width/2
      self._d_target_output.data.position.y = -(float(mato_point[1]) - self.height/2)
      for i in circles[0,:]:
        # draw the outer circle
        cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
        # draw the center of the circle
        cv2.circle(img,(i[0],i[1]),2,(0,0,255),3)

    img2 = cv2.resize(img , (int(self.width*0.3), int(self.height*0.3)))
    gray2 = cv2.resize(gray , (int(self.width*0.3), int(self.height*0.3)))
    cv2.imshow("viewer", img2)

    if cv2.waitKey(1) > 0:
      cv2.destroyAllWindows()
    
    # to do
    print(self._d_target_output)
    self._target_outputOut.write()

    return RTC.RTC_OK

  ###
  ##
  ## The aborting action when main logic error occurred.
  ## former rtc_aborting_entry()
  ##
  ## @param ec_id target ExecutionContext Id
  ##
  ## @return RTC::ReturnCode_t
  ##
  ##
  #def onAborting(self, ec_id):
  #
  #  return RTC.RTC_OK

  ###
  ##
  ## The error action in ERROR state
  ## former rtc_error_do()
  ##
  ## @param ec_id target ExecutionContext Id
  ##
  ## @return RTC::ReturnCode_t
  ##
  ##
  #def onError(self, ec_id):
  #
  #  return RTC.RTC_OK

  ###
  ##
  ## The reset action that is invoked resetting
  ## This is same but different the former rtc_init_entry()
  ##
  ## @param ec_id target ExecutionContext Id
  ##
  ## @return RTC::ReturnCode_t
  ##
  ##
  #def onReset(self, ec_id):
  #
  #  return RTC.RTC_OK

  ###
  ##
  ## The state update action that is invoked after onExecute() action
  ## no corresponding operation exists in OpenRTm-aist-0.2.0
  ##
  ## @param ec_id target ExecutionContext Id
  ##
  ## @return RTC::ReturnCode_t
  ##

  ##
  #def onStateUpdate(self, ec_id):
  #
  #  return RTC.RTC_OK

  ###
  ##
  ## The action that is invoked when execution context's rate is changed
  ## no corresponding operation exists in OpenRTm-aist-0.2.0
  ##
  ## @param ec_id target ExecutionContext Id
  ##
  ## @return RTC::ReturnCode_t
  ##
  ##
  #def onRateChanged(self, ec_id):
  #
  #  return RTC.RTC_OK




def MatoDetectorInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=matodetector_spec)
    manager.registerFactory(profile,
                            MatoDetector,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    MatoDetectorInit(manager)

    # Create a component
    comp = manager.createComponent("MatoDetector")

def main():
  mgr = OpenRTM_aist.Manager.init(sys.argv)
  mgr.setModuleInitProc(MyModuleInit)
  mgr.activateManager()
  mgr.runManager()

if __name__ == "__main__":
  main()

