#include <ros/ros.h>
#include <ros/package.h>
#include <sensor_msgs/JointState.h>
#include <liancheng_socket/MotorOrder.h>
#include <liancheng_socket/SwitchOrder.h>
#include <liancheng_socket/ReadOutput.h>
#include <std_msgs/UInt8MultiArray.h>
#include <serial/serial.h>
#include <string.h>
#include <iostream>

using namespace std;

int main (int argc, char** argv)
{
    ros::init( argc, argv, "talker" );
    ros::NodeHandle nh;
    ros::Rate rate(1.0);

    ros::Publisher pub=nh.advertise<liancheng_socket::MotorOrder>("Controller_motor_order",5);
	ros::Publisher pub2=nh.advertise<liancheng_socket::MotorOrder>("CANController_motor_order",5);
    ros::Publisher pub_sw=nh.advertise<liancheng_socket::SwitchOrder>("Controller_switch_order",5);
	ros::Publisher pub_read=nh.advertise<liancheng_socket::ReadOutput>("Read_motor",5);
    rate.sleep();

    

    

	while(1){
		liancheng_socket::MotorOrder msg;
		liancheng_socket::MotorOrder msg_can;
		liancheng_socket::SwitchOrder msg_sw;
		liancheng_socket::ReadOutput msg_read;

		string rec;
    	cin>>rec;
		if (rec=="1")
			{
				msg_can.header.stamp=ros::Time::now();
				msg_can.station_num.push_back(3);
				msg_can.station_num.push_back(5);
				msg_can.form.push_back(1);
				msg_can.vel.push_back(500);
				msg_can.vel_ac.push_back(1);
				msg_can.vel_de.push_back(0);
				msg_can.pos_mode.push_back(0);
				msg_can.pos.push_back(-300);
				msg_can.pos_thr.push_back(0);
				cout<<"11"<<endl;
				pub2.publish(msg_can);
			}
			else if (rec=="2")
			{
				msg_can.header.stamp=ros::Time::now();
				msg_can.station_num.push_back(3);
				msg_can.station_num.push_back(5);
				msg_can.form.push_back(0);
				msg_can.vel.push_back(500);
				msg_can.vel_ac.push_back(1);
				msg_can.vel_de.push_back(0);
				msg_can.pos_mode.push_back(0);
				msg_can.pos.push_back(-300);
				msg_can.pos_thr.push_back(0);
				pub2.publish(msg_can);
				cout<<"10"<<endl;
			}
			else if (rec=="66")
			{
				msg_can.header.stamp=ros::Time::now();
				msg_can.station_num.push_back(3);
				msg_can.station_num.push_back(5);
				msg_can.form.push_back(1);
				msg_can.vel.push_back(500);
				msg_can.vel_ac.push_back(2);
				msg_can.vel_de.push_back(0);
				msg_can.pos_mode.push_back(0);
				msg_can.pos.push_back(-300);
				msg_can.pos_thr.push_back(0);
				pub2.publish(msg_can);
				cout<<"21"<<endl;
			}
			else if (rec=="67")
			{
				msg_can.header.stamp=ros::Time::now();
				msg_can.station_num.push_back(3);
				msg_can.station_num.push_back(5);
				msg_can.form.push_back(0);
				msg_can.vel.push_back(500);
				msg_can.vel_ac.push_back(2);
				msg_can.vel_de.push_back(0);
				msg_can.pos_mode.push_back(0);
				msg_can.pos.push_back(-300);
				msg_can.pos_thr.push_back(0);
				pub2.publish(msg_can);
				cout<<"20"<<endl;
			}
			// feed motor 485
            else if(rec=="3")
            {
				msg.header.stamp=ros::Time::now();
				msg.station_num.push_back(1);
				msg.form.push_back(100);
				msg.vel.push_back(50);
				msg.vel_ac.push_back(10);
				msg.vel_de.push_back(0);
				msg.pos_mode.push_back(false);
				msg.pos.push_back(0);
				msg.pos_thr.push_back(10);
				
				msg.station_num.push_back(1);
				msg.form.push_back(0);
				msg.vel.push_back(50);
				msg.vel_ac.push_back(10);
				msg.vel_de.push_back(0);
				msg.pos_mode.push_back(true);
				msg.pos.push_back(0);
				msg.pos_thr.push_back(10);

				msg.station_num.push_back(1);
				msg.form.push_back(99);
				msg.vel.push_back(50);
				msg.vel_ac.push_back(10);
				msg.vel_de.push_back(0);
				msg.pos_mode.push_back(false);
				msg.pos.push_back(0);
				msg.pos_thr.push_back(10);
				cout<<"333"<<endl;
				pub.publish(msg);
			}
			else if (rec=="4")
			{
				msg.header.stamp=ros::Time::now();
				msg.station_num.push_back(1);
				msg.form.push_back(100);
				msg.vel.push_back(50);
				msg.vel_ac.push_back(10);
				msg.vel_de.push_back(0);
				msg.pos_mode.push_back(true);
				msg.pos.push_back(0);
				msg.pos_thr.push_back(10);
				
				// msg.station_num.push_back(1);
				// msg.form.push_back(0);
				// msg.vel.push_back(50);
				// msg.vel_ac.push_back(10);
				// msg.vel_de.push_back(0);
				// msg.pos_mode.push_back(false);
				// msg.pos.push_back(200);
				// msg.pos_thr.push_back(10);

				// msg.station_num.push_back(1);
				// msg.form.push_back(99);
				// msg.vel.push_back(50);
				// msg.vel_ac.push_back(10);
				// msg.vel_de.push_back(0);
				// msg.pos_mode.push_back(false);
				// msg.pos.push_back(0);
				// msg.pos_thr.push_back(10);
				// cout<<"444"<<endl;
				pub.publish(msg);
			}

			else if (rec=="99")
			{
				msg.header.stamp=ros::Time::now();
				msg.station_num.push_back(3);
				msg.form.push_back(99);
				msg.vel.push_back(1000);
				msg.vel_ac.push_back(0);
				msg.vel_de.push_back(0);
				msg.pos_mode.push_back(true);
				msg.pos.push_back(0);
				msg.pos_thr.push_back(10);
                msg.station_num.push_back(1);
				msg.form.push_back(99);
				msg.vel.push_back(1000);
				msg.vel_ac.push_back(0);
				msg.vel_de.push_back(0);
				msg.pos_mode.push_back(true);
				msg.pos.push_back(0);
				msg.pos_thr.push_back(10);
				cout<<"999"<<endl;
			}
			else if (rec=="100")
			{
				msg.header.stamp=ros::Time::now();
				msg.station_num.push_back(3);
				msg.form.push_back(100);
				msg.vel.push_back(1000);
				msg.vel_ac.push_back(0);
				msg.vel_de.push_back(0);
				msg.pos_mode.push_back(true);
				msg.pos.push_back(0);
				msg.pos_thr.push_back(10);
                msg.station_num.push_back(1);
				msg.form.push_back(100);
				msg.vel.push_back(1000);
				msg.vel_ac.push_back(0);
				msg.vel_de.push_back(0);
				msg.pos_mode.push_back(true);
				msg.pos.push_back(0);
				msg.pos_thr.push_back(10);
				cout<<"100"<<endl;
			}
			// pinch motor can
			else if (rec=="101")
			{
				msg_can.header.stamp=ros::Time::now();
				msg_can.station_num.push_back(1);
				msg_can.station_num.push_back(0x41);
				msg_can.form.push_back(200);
				msg_can.vel.push_back(100);
				msg_can.vel_ac.push_back(0);
				msg_can.vel_de.push_back(0);
				msg_can.pos_mode.push_back(0);
				msg_can.pos.push_back(-1);
				msg_can.pos_thr.push_back(0);
				cout<<"can"<<endl;
				pub2.publish(msg_can);
			}
			else if (rec=="102")
			{
				msg_can.header.stamp=ros::Time::now();
				msg_can.station_num.push_back(1);
				msg_can.station_num.push_back(0x41);
				msg_can.form.push_back(199);
				msg_can.vel.push_back(100);
				msg_can.vel_ac.push_back(0);
				msg_can.vel_de.push_back(0);
				msg_can.pos_mode.push_back(0);
				msg_can.pos.push_back(-2000);
				msg_can.pos_thr.push_back(0);
				cout<<"can"<<endl;
				pub2.publish(msg_can);
			}
			// pinch motor 485
			else if (rec=="103")
			{
				msg_can.header.stamp=ros::Time::now();
				msg_can.station_num.push_back(1);
				msg_can.form.push_back(200);
				msg_can.vel.push_back(100);
				msg_can.vel_ac.push_back(0);
				msg_can.vel_de.push_back(0);
				msg_can.pos_mode.push_back(0);
				msg_can.pos.push_back(-5000);
				msg_can.pos_thr.push_back(0);
				cout<<"485"<<endl;
				pub.publish(msg_can);
			}
			else if (rec=="104")
			{
				msg_can.header.stamp=ros::Time::now();
				msg_can.station_num.push_back(1);
				msg_can.form.push_back(200);
				msg_can.vel.push_back(100);
				msg_can.vel_ac.push_back(0);
				msg_can.vel_de.push_back(0);
				msg_can.pos_mode.push_back(0);
				msg_can.pos.push_back(5000);
				msg_can.pos_thr.push_back(0);
				cout<<"485"<<endl;
				pub.publish(msg_can);
			}
			// x,y motor test
			else if(rec=="111")// x relative move
            {
				msg_can.header.stamp=ros::Time::now();
				msg_can.station_num.push_back(2);
				msg_can.station_num.push_back(0x01);
				msg_can.form.push_back(12);
				msg_can.vel.push_back(100);
				msg_can.vel_ac.push_back(0);
				msg_can.vel_de.push_back(0);
				msg_can.pos_mode.push_back(true);
				msg_can.pos.push_back(300*1000);// 1mm -> 1000
				msg_can.pos_thr.push_back(10);
				cout<<"111"<<endl;
				pub2.publish(msg_can);
			}
			else if (rec=="112")// x absolute move
			{
				msg_can.header.stamp=ros::Time::now();
				msg_can.station_num.push_back(2);
				msg_can.station_num.push_back(0x01);
				msg_can.form.push_back(11);
				msg_can.vel.push_back(100);
				msg_can.vel_ac.push_back(0);
				msg_can.vel_de.push_back(0);
				msg_can.pos_mode.push_back(true);
				msg_can.pos.push_back(0);
				msg_can.pos_thr.push_back(10);
				cout<<"112"<<endl;
				pub2.publish(msg_can);
			}
			else if(rec=="113")// x relative move
            {
				msg_can.header.stamp=ros::Time::now();
				msg_can.station_num.push_back(2);
				msg_can.station_num.push_back(0x02);
				msg_can.form.push_back(12);
				msg_can.vel.push_back(100);
				msg_can.vel_ac.push_back(0);
				msg_can.vel_de.push_back(0);
				msg_can.pos_mode.push_back(true);
				msg_can.pos.push_back(-300*1000);// 1mm -> 1000
				msg_can.pos_thr.push_back(10);
				cout<<"113"<<endl;
				pub2.publish(msg_can);
			}
			else if (rec=="114")// x absolute move
			{
				msg_can.header.stamp=ros::Time::now();
				msg_can.station_num.push_back(2);
				msg_can.station_num.push_back(0x02);
				msg_can.form.push_back(11);
				msg_can.vel.push_back(100);
				msg_can.vel_ac.push_back(0);
				msg_can.vel_de.push_back(0);
				msg_can.pos_mode.push_back(true);
				msg_can.pos.push_back(0);
				msg_can.pos_thr.push_back(10);
				cout<<"114"<<endl;
				pub2.publish(msg_can);
			}
			
			else if(rec=="211")
            {
				msg_can.header.stamp=ros::Time::now();
				msg_can.station_num.push_back(7);
				msg_can.form.push_back(12);
				msg_can.vel.push_back(100);
				msg_can.vel_ac.push_back(0);
				msg_can.vel_de.push_back(0);
				msg_can.pos_mode.push_back(true);
				msg_can.pos.push_back(200);
				msg_can.pos_thr.push_back(10);
				cout<<"211x211"<<endl;
				pub2.publish(msg_can);
			}
			else if (rec=="212")
			{
				msg_can.header.stamp=ros::Time::now();
				msg_can.station_num.push_back(7);
				msg_can.form.push_back(12);
				msg_can.vel.push_back(100);
				msg_can.vel_ac.push_back(0);
				msg_can.vel_de.push_back(0);
				msg_can.pos_mode.push_back(true);
				msg_can.pos.push_back(0);
				msg_can.pos_thr.push_back(10);
				cout<<"212x212"<<endl;
				pub2.publish(msg_can);
			}
			else if (rec=="999")
			{
				msg.header.stamp=ros::Time::now();
				msg.station_num.push_back(2);
				msg.form.push_back(200);
				msg.vel.push_back(100);
				msg.vel_ac.push_back(0);
				msg.vel_de.push_back(0);
				msg.pos_mode.push_back(true);
				msg.pos.push_back(36000);
				msg.pos_thr.push_back(10);
				cout<<"212x212"<<endl;
			}
			else if (rec=="998")
			{
				msg.header.stamp=ros::Time::now();
				msg.station_num.push_back(2);
				msg.form.push_back(200);
				msg.vel.push_back(100);
				msg.vel_ac.push_back(0);
				msg.vel_de.push_back(0);
				msg.pos_mode.push_back(true);
				msg.pos.push_back(0);
				msg.pos_thr.push_back(10);
				cout<<"212x212"<<endl;
			}
			else if (rec=="1000")
			{
				msg_read.header.stamp=ros::Time::now();
				msg_read.station_num = 0x02;
				msg_read.data = 100;
				cout<<"113x113"<<endl;
				pub_read.publish(msg_read);
			}
			else break;
			// else if (rec=="114")
			// {
			// 	msg_sw.header.stamp=ros::Time::now();
			// 	msg_sw.station_num.push_back(7);
			// 	msg_sw.switch_num.push_back(16);
			// 	msg_sw.t.push_back(false);
			// 	cout<<"114x114"<<endl;
			// }
			// else if (rec=="115")
			// {
			// 	msg_sw.header.stamp=ros::Time::now();
			// 	msg_sw.station_num.push_back(7);
			// 	msg_sw.switch_num.push_back(18);
			// 	msg_sw.t.push_back(true);
			// 	cout<<"115x115"<<endl;
			// }
			// else if (rec=="116")
			// {
			// 	msg_sw.header.stamp=ros::Time::now();
			// 	msg_sw.station_num.push_back(7);
			// 	msg_sw.switch_num.push_back(18);
			// 	msg_sw.t.push_back(false);
			// 	cout<<"116x116"<<endl;
			// }
			// pub.publish(msg);
			// pub2.publish(msg_can);
			// pub_sw.publish(msg_sw);
			
			
    
    
    ros::spinOnce();
	}

    
    return 0;
}
