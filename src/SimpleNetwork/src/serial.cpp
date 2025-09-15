#include <iostream>
#include <signal.h>
#include "RS485Serial.h"

int main(int argc, char **argv){
    
    ROS_INFO("starting");
    ros::init( argc,argv, "serial" );
    ros::NodeHandle nh;
    serialpublisher serialpub(nh);
    
    serialpub.init();

    ros::Rate rate(10.0);
    ros::spin();
    
    return 0;
}


