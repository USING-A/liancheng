#include "RS485Serial.h"

serialpublisher::serialpublisher(ros::NodeHandle & nh){
        nh_=nh;
        to = serial::Timeout::simpleTimeout(3000);
        baud=115200;//进给电机上位机修改为115200
        port="/dev/ttyUSB0";
        // ros::param::get("port1",port,"/dev/ttyUSB0");
        // port="/dev/ttyTHS0";

        sub=nh_.subscribe("/Controller_motor_order",5,&serialpublisher::callback,this);
        sub_sw=nh_.subscribe("/Controller_switch_order",5,&serialpublisher::callback_sw,this);
        // sub_read=nh_.subscribe("/Read_motor",5,&serialpublisher::callback_read,this);
        pub_read=nh_.advertise<liancheng_socket::ReadOutput>("Read_motor_output",5);


    /*
    code list:
    0->DI1=enable/DI1端口关联使能;
    1->enable on/使能开;
    2->enable off/使能关;
    3->control model:vel/控制模式：速度控制;
    4->control model:pos/控制模式：位移控制;
    5->vel order from:internal vel/速度指令来源：内部速度指令;
    6->DI2=pos enable/DI2端口关联位移运行使能;
    7->pos enable on/位移运行使能开;
    8->pos enable off/位移运行使能关;
    9->DO1=pos arrived/DO1端口关联定位到达;
    10->DO1 positive/定位到达正逻辑;
    11->pos order from:internal pos/位置指令来源：内部位移指令;
    12->pos from:once/多段位置运行方式：单次运行;
    13->pos num:1/位移指令段数:1段;
    14->absolute pos/绝对位移模式;
    15->relative pos/相对位移模式;
    16->read vel/读取转速;
    17->read pos/读取位置;
    18->read input/读取输入端口情况;
    19->read output/读取输出端口情况;
    20->read current/读取相电流;
    21->read voltage/读取母线电压;
    22->read temperature/读取模块温度;
    23->读取俯仰电机多圈角度
    24->进给电机零位设置（当前位置作为零点）
    */
    // vector<vector<uint8_t>> code_list(25); //不能加 否则电机指令码会异常
    code_list[0]={0x06,0x03,0x02,0x00,0x01};//06 写,03 读
    code_list[1]={0x06,0x03,0x03,0x00,0x01};
    code_list[2]={0x06,0x03,0x03,0x00,0x00};
    code_list[3]={0x06,0x02,0x00,0x00,0x00};
    code_list[4]={0x06,0x02,0x00,0x00,0x01};
    code_list[5]={0x06,0x06,0x02,0x00,0x00};
    code_list[6]={0x06,0x03,0x04,0x00,0x1c};
    code_list[7]={0x06,0x03,0x05,0x00,0x01};
    code_list[8]={0x06,0x03,0x05,0x00,0x00};
    code_list[9]={0x06,0x04,0x00,0x00,0x05};
    code_list[10]={0x06,0x04,0x01,0x00,0x00};
    code_list[11]={0x06,0x05,0x00,0x00,0x02};
    code_list[12]={0x06,0x11,0x00,0x00,0x00};
    code_list[13]={0x06,0x11,0x01,0x00,0x01};
    code_list[14]={0x06,0x11,0x04,0x00,0x01};
    code_list[15]={0x06,0x11,0x04,0x00,0x00};
    code_list[16]={0x03,0x0b,0x00,0x00,0x01};
    code_list[17]={0x03,0x0b,0x07,0x00,0x02};
    code_list[18]={0x03,0x0b,0x03,0x00,0x01};
    code_list[19]={0x03,0x0b,0x05,0x00,0x01};
    code_list[20]={0x03,0x0b,0x18,0x00,0x01};
    code_list[21]={0x03,0x0b,0x1a,0x00,0x01};
    code_list[22]={0x03,0x0b,0x1b,0x00,0x01};

    code_list[23]={};
    code_list[24]={0x06,0x03,0x07,0x00,0x01};//写入当前位置作为零点 DI3
    code_list[25]={0x06,0x03,0x08,0x00,0x12};//正向点动 DI4
    code_list[26]={0x06,0x03,0x10,0x00,0x13};//负向点动 DI5
    code_list[27]={0x06,0x03,0x07,0x00,0x01};//DI3 使能开
    code_list[28]={0x06,0x03,0x07,0x00,0x00};//DI3 使能关
    code_list[29]={0x06,0x03,0x09,0x00,0x01};//DI4 使能开
    code_list[30]={0x06,0x03,0x09,0x00,0x00};//DI4 使能关
    code_list[31]={0x06,0x03,0x11,0x00,0x01};//DI5 使能开
    code_list[32]={0x06,0x03,0x11,0x00,0x00};//DI5 使能关
    /*
    俯仰电机485方案
    0->相对位移运动模式
    1->绝对位移运动模式
    2->设置当前位置为零点
    */
    pinch_list[0]={0x3e,0x08,0xa8,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00};
    pinch_list[1]={0x3e,0x08,0xa4,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00};
    pinch_list[2]={0x3e,0x08,0x64,0x00,0x00,0x00,0x00,0x00,0x00,0x00};

    
    try
    {
    //set the property of the port and open it.
        ser.setPort(port);
        ser.setBaudrate(baud);
        ser.setTimeout(to);
        ser.open();
    }
    catch (serial::IOException &e)
    {
        ROS_ERROR_STREAM("Unable to open port ");       
        //return -1;
    }
    catch(serial::SerialException &e)
    {
      ROS_ERROR_STREAM("Serial port already open. ");       
    }



    }

serialpublisher::~serialpublisher(){}

void serialpublisher::init() {
    // 创建一个定时器，每100ms触发一次读取
    readTimer = nh_.createTimer(ros::Duration(0.1), &serialpublisher::timerCallback, this);
    heartbeatTimer = nh_.createTimer(ros::Duration(1.0), &serialpublisher::heartbeatCallback, this);
}

void serialpublisher::timerCallback(const ros::TimerEvent&)
{
    liancheng_socket::ReadOutput order;
    order.station_num = 1;  // 读取俯仰电机
    callback_read(order); 

    order.station_num = 2;  // 读取伸缩电机
    callback_read(order);
}

void serialpublisher::heartbeatCallback(const ros::TimerEvent&)
{
    heartbeat_check();
}

void serialpublisher::prepare()
{
    while(!ser.isOpen())
    {
        port="/dev/ttyUSB1";
    try
    {
    //set the property of the port and open it.
        ser.setPort(port);
        ser.setBaudrate(baud);
        ser.setTimeout(to);
        ser.open();
    }
    catch (serial::IOException &e)
    {
        ROS_ERROR_STREAM("Unable to open port ");       
    }
     catch(serial::SerialException &e)
    {
      ROS_ERROR_STREAM("Serial port already open. ");       
    }

    sleeptime.sleep();
    port="/dev/ttyUSB0";
    try
    {
    //set the property of the port and open it.
        ser.setPort(port);
        ser.setBaudrate(baud);
        ser.setTimeout(to);
        ser.open();
    }
    catch (serial::IOException &e)
    {
        ROS_ERROR_STREAM("Unable to open port ");       
    }
     catch(serial::SerialException &e)
    {
      ROS_ERROR_STREAM("Serial port already open. ");       
    }

    }

    sleeptime.sleep();

    ROS_INFO("Connected !");
    ROS_INFO("End preparation");

}

bool serialpublisher::set_form(uint8_t station_num,int8_t form_input)
{

    if (form==form_input)
    {
        return true;
    }
    int *code_order;
    int code_num;
    
    if (form_input==1)
    {
        code_num=6;
        code_order=new int[code_num]{3,0,2,5,6,8};
    }
    else if (form_input==0)
    {
        code_num=10;
        code_order=new int[code_num]{4,0,2,6,8,9,10,11,12,13};
    }
    else
    {
        cout<<"form input error"<<endl;
        return false;
    }

    for (int i=0;i<code_num;i++)
    {
        ser.write(CRC16_MudBus(code_list[code_order[i]],code_list[code_order[i]].size(),station_num));
        sleeptime_code.sleep();
    }

    form=form_input;
    return true;
}

void serialpublisher::vel_form(uint8_t station_num,int16_t vel, uint16_t vel_ac,uint16_t vel_de){

    if (form!=1)
    {
        set_form(station_num,1);
    }
    if (vel > 6000)
    {
        vel=6000;
    }
    if (vel < -6000)
    {
        vel=-6000;
    }
    vector<uint8_t> code5={0x06,0x06,0x03,uint8_t(vel>>8),uint8_t(vel&0x00ff)};
    vector<uint8_t> code6={0x06,0x06,0x05,uint8_t(vel_ac>>8),uint8_t(vel_ac&0x00ff)};
    vector<uint8_t> code7={0x06,0x06,0x06,uint8_t(vel_de>>8),uint8_t(vel_de&0x00ff)};
    
    ser.write(CRC16_MudBus(code5,code5.size(),station_num));
    sleeptime_code.sleep();
    ser.write(CRC16_MudBus(code6,code6.size(),station_num));
    sleeptime_code.sleep();
    ser.write(CRC16_MudBus(code7,code7.size(),station_num));
    sleeptime_code.sleep();
    cout<<"vel_form set successfully!"<<endl;
    cout<<"station num="<<station_num<<endl;
    cout<<"set vel="<<vel<<endl;
    cout<<"set vel_ac="<<vel_ac<<endl;
    cout<<"set vel_de="<<vel_de<<endl;

}

void serialpublisher::pos_form(uint8_t station_num,bool pos_mode,int32_t pos, uint16_t pos_thr ,uint16_t vel,uint16_t vel_ac){

    if (form!=0)
    {
        set_form(station_num,0);
    }
    // if (pos>0)
    // {
    //     pos=0;
    // }
    if (pos<-7000)
    {
        pos=-7000;
    }
    vector<uint8_t> code1={0x06,0x05,0x15,uint8_t(pos_thr>>8),uint8_t(pos_thr&0x00ff)};
    int16_t pos_high=int16_t(pos>>16);
    int16_t pos_low=int16_t(pos&0x0000ffff);
    
    vector<uint8_t> code2={0x10,0x11,0x0c,0x00,0x04,0x08,uint8_t(pos_low>>8),uint8_t(pos_low&0x00ff),uint8_t(pos_high>>8),uint8_t(pos_high&0x00ff),uint8_t(vel>>8),uint8_t(vel&0x00ff),uint8_t(vel_ac>>8),uint8_t(vel_ac&0x00ff)};

    if (pos_mode)
    {
        ser.write(CRC16_MudBus(code_list[14],code_list[14].size(),station_num));
        sleeptime_code.sleep();
    }
    else
    {
        ser.write(CRC16_MudBus(code_list[15],code_list[15].size(),station_num));
        sleeptime_code.sleep();
    }
    
    ser.write(CRC16_MudBus(code1,code1.size(),station_num));
    sleeptime_code.sleep();
    ser.write(CRC16_MudBus(code2,code2.size(),station_num));
    sleeptime_code.sleep();
    // 先关一次位移使能，再启用
    ser.write(CRC16_MudBus(code_list[8],code_list[8].size(),station_num));
    sleeptime_code.sleep();
    ser.write(CRC16_MudBus(code_list[7],code_list[7].size(),station_num));
    sleeptime_code.sleep();
    cout<<"pos_form set successfully!"<<endl;
    cout<<"station num="<<station_num<<endl;
    if (pos_mode)
    {
        cout<<"set pos_mode=absolute pos"<<endl;
    }
    else
    {
        cout<<"set pos_mode=relative pos"<<endl;
    }
    // cout<<"########"<<std::hex<<(pos_low>>8)<<"+"<<std::hex<<(pos_low&0x00ff)<<"+"<<std::hex<<(pos_high>>8)<<"+"<<std::hex<<(pos_high&0x00ff)<<endl;
    cout<<"set pos="<<pos<<endl;
    cout<<"set pos_thr="<<pos_thr<<endl;
    cout<<"set vel="<<vel<<endl;
    cout<<"set vel_ac="<<vel_ac<<endl;
}

void serialpublisher::switch_ch(uint8_t station_num, uint16_t switch_num, uint8_t case_num)
{
    vector<uint8_t> code1={0x06,uint8_t(switch_num>>8),uint8_t(switch_num&0x00ff),0,case_num};
    ser.write(CRC16_MudBus(code1,code1.size(),station_num));
    sleeptime_code.sleep();
}

void serialpublisher::enable_on(uint8_t station_num)
{
    ser.write(CRC16_MudBus(code_list[1],code_list[1].size(),station_num));
    sleeptime_code.sleep();
    cout<<"enable on set successfully!"<<endl;
    cout<<"station num="<<station_num<<endl;
}

void serialpublisher::enable_off(uint8_t station_num)
{
    ser.write(CRC16_MudBus(code_list[2],code_list[2].size(),station_num));
    sleeptime_code.sleep();
    cout<<"enable off set successfully!"<<endl;
    cout<<"station num="<<station_num<<endl;
}


void serialpublisher::set_current_arm_pos_as_zero(uint8_t station_num)
{
    if (form!=2){set_form(station_num,2);}
    vector<uint8_t> code1={0x06,0x03,0x07,0x00,0x00};
    vector<uint8_t> code2={0x06,0x03,0x07,0x00,0x01};
    ser.write(CRC16_MudBus(code1,code1.size(),station_num));
    sleeptime_code.sleep();
    ser.write(CRC16_MudBus(code2,code2.size(),station_num));
    sleeptime_code.sleep();
    ser.write(CRC16_MudBus(code1,code1.size(),station_num));
    sleeptime_code.sleep();
    cout<<"set current arm pos as zero successfully!"<<endl;
    cout<<"station num="<<station_num<<endl;
}

void serialpublisher::set_current_pitch_pos_as_zero(uint8_t station_num)
{
    ser.write(CRC16_MudBus2(pinch_list[2],pinch_list[2].size(),station_num));
    sleeptime_code.sleep();
    vector<uint8_t> code1={0x3E,0x08,0x76,0x00,0x00,0x00,0x00,0x00,0x00,0x00};// 系统复位指令
    ser.write(CRC16_MudBus2(code1,code1.size(),station_num));
    sleeptime_code.sleep();
    cout<<"set current pitch pos as zero successfully!"<<endl;
    cout<<"station num="<<station_num<<endl;
}

void serialpublisher::pos_pitch(uint8_t station_num,bool pos_mode,int16_t vel,int32_t pos)
{
    // if (pos>1000)
    // {
    //     pos=1000;
    // }
    // if (pos<-3000)
    // {
    //     pos=-3000;
    // }
    int16_t pos_high=int16_t(pos>>16);
    int16_t pos_low=int16_t(pos&0x0000ffff);
    // pos_mode==1 : absolute; pos_mode==0 : relative
    if (pos_mode)
    {
        vector<uint8_t> pinch_code1={0x3e,0x08,0xa4,0x00,uint8_t(vel&0x00ff),uint8_t(vel>>8),uint8_t(pos_low&0x00ff),uint8_t(pos_low>>8),uint8_t(pos_high&0x00ff),uint8_t(pos_high>>8)};
        ser.write(CRC16_MudBus2(pinch_code1,pinch_code1.size(),station_num));
        sleeptime_code.sleep();
        cout<<"pinch motor absolutely move!"<<endl;
    }
    else
    {
        vector<uint8_t> pinch_code2={0x3e,0x08,0xa8,0x00,uint8_t(vel&0x00ff),uint8_t(vel>>8),uint8_t(pos_low&0x00ff),uint8_t(pos_low>>8),uint8_t(pos_high&0x00ff),uint8_t(pos_high>>8)};
        ser.write(CRC16_MudBus2(pinch_code2,pinch_code2.size(),station_num));
        sleeptime_code.sleep();
        cout<<"pinch motor relatively move!"<<endl;
    }
    cout<<"station num="<<station_num<<endl;
    cout<<"set vel="<<vel<<endl;
    cout<<"set pos="<<pos<<endl;

}

void serialpublisher::callback(const liancheng_socket::MotorOrder & order)
{
    int order_num=order.station_num.size();
    
    for (int i=0;i<order_num;i++)
    {
        uint8_t station_num=order.station_num[i];
        uint8_t form=order.form[i];
        int16_t vel=order.vel[i];
        uint16_t vel_ac=order.vel_ac[i];
        uint16_t vel_de=order.vel_de[i];
        bool pos_mode=order.pos_mode[i];
        int32_t pos=order.pos[i];
        uint16_t pos_thr=order.pos_thr[i];
        switch (form)
        {
            case 0:
            this->pos_form(station_num,pos_mode,pos*10, pos_thr,vel,vel_ac); // 10 LSB -> 1 mm
            continue;

            case 1:
            this->vel_form(station_num,vel,vel_ac,vel_de);
            continue;

            case 2:
            this->set_current_arm_pos_as_zero(station_num);

            case 99:
            this->enable_on(station_num);
            continue;

            case 100:
            this->enable_off(station_num);
            continue;

            case 201:
            this->set_current_pitch_pos_as_zero(station_num);
            continue;

            case 200:
            this->pos_pitch(station_num,pos_mode,vel,pos*100);//100 LSB -> 1 degree
            continue;

        }

    return;
}
}

void serialpublisher::callback_read(const liancheng_socket::ReadOutput & order)
{
    uint8_t station_num=order.station_num;
    int num,enable_state,pos,vel,check = 1;
    vector<uint8_t> data_list;
    
    if (station_num==1)
    {
        vector<uint8_t> code1={0x3E,0x08,0x9A,0x00,0x00,0x00,0x00,0x00,0x00,0x00};// 读取俯仰电机使能状态
        ser.write(CRC16_MudBus2(code1,code1.size(),station_num));
        sleeptime_code.sleep();
        num=ser.available();
        if (num > 0) {
            size_t read_size = ser.read(data_list, num);
            if (read_size != num) {
                ROS_ERROR_STREAM("Failed to read all data from serial port.");
                return;
            }
        } 
        else {
            ROS_ERROR_STREAM("No data available on serial port.");
            return;
        }
        if (data_list[0]!=0x3E || data_list[1]!= 0x01 || data_list[2]!=0x08 || data_list[3]!=0x9A){
            ROS_ERROR_STREAM("Receive wrong data list:");
            for(size_t i=0;i<sizeof(data_list)/sizeof(data_list[0]);i++)
                printf("%02X,",data_list[i]);
            data_list.clear();
            check = 0;
        }
        else{
            enable_state=data_list[6];// 使能状态,1使能,0未使能
            data_list.clear();
        }


        vector<uint8_t> code2={0x3E,0x08,0x9C,0x00,0x00,0x00,0x00,0x00,0x00,0x00};// 读取俯仰电机速度
        ser.write(CRC16_MudBus2(code2,code2.size(),station_num));
        sleeptime_code.sleep();
        num=ser.available();
        if (num > 0) {
            size_t read_size = ser.read(data_list, num);
            if (read_size != num) {
                ROS_ERROR_STREAM("Failed to read all data from serial port.");
                return;
            }
        } 
        else {
            ROS_ERROR_STREAM("No data available on serial port.");
            return;
        }
        if (data_list[0]!=0x3E || data_list[1]!= 0x01 || data_list[2]!=0x08 || data_list[3]!=0x9C){
            ROS_ERROR_STREAM("Receive wrong data list:");
            for(size_t i=0;i<sizeof(data_list)/sizeof(data_list[0]);i++)
                printf("%02X,",data_list[i]);
            data_list.clear();
            check = 0;
        }
        else{
            vel=data_list[8]*256+data_list[7];// 速度
            data_list.clear();
        }


        vector<uint8_t> code3={0x3E,0x08,0x92,0x00,0x00,0x00,0x00,0x00,0x00,0x00};// 读取俯仰电机位置
        ser.write(CRC16_MudBus2(code3,code3.size(),station_num));
        sleeptime_code.sleep();
        num=ser.available();
        if (num > 0) {
            size_t read_size = ser.read(data_list, num);
            if (read_size != num) {
                ROS_ERROR_STREAM("Failed to read all data from serial port.");
                return;
            }
        } 
        else {
            ROS_ERROR_STREAM("No data available on serial port.");
            return;
        }
        if (data_list[0]!=0x3E || data_list[1]!= 0x01 || data_list[2]!=0x08 || data_list[3]!=0x92){
            ROS_ERROR_STREAM("Receive wrong data list:");
            for(size_t i=0;i<sizeof(data_list)/sizeof(data_list[0]);i++)
                printf("%02X,",data_list[i]);
            data_list.clear();
            check = 0;
        }
        else{
            pos=(data_list[7]+data_list[8]*256+data_list[9]*256*256+data_list[10]*256*256*256);// 位置
            data_list.clear();
        }

        if(check){
            nh_.setParam("/read_pitch_motor_enable_status", enable_state);// 设置俯仰电机使能状态参数
            nh_.setParam("/read_pitch_motor_position", pos*0.01);// 设置俯仰电机位置参数 100 LSB ->1 degree
            nh_.setParam("/read_pitch_motor_speed", vel);// 设置俯仰电机速度参数
            cout<<"pitch motor enable state="<<enable_state<<endl;
            cout<<"pitch motor pos="<<pos*0.01<<endl;
            cout<<"pitch motor vel="<<vel<<endl;
            cout<<"Read output successfully!"<<endl;
        }

    }
    else if (station_num==2)
    {
        vector<uint8_t> code1={0x03,0x0B,0x07,0x00,0x02};// 读取伸缩电机位置
        ser.write(CRC16_MudBus(code1,code1.size(),station_num));
        sleeptime_code.sleep();
        num=ser.available();
        if (num > 0) {
            size_t read_size = ser.read(data_list, num);
            if (read_size != num) {
                ROS_ERROR_STREAM("Failed to read all data from serial port.");
                return;
            }
        } 
        else {
            ROS_ERROR_STREAM("No data available on serial port.");
            return;
        }
        if (data_list[0]!=0x02 || data_list[1]!= 0x03){
            ROS_ERROR_STREAM("Receive wrong data list:");
            for(size_t i=0;i<sizeof(data_list)/sizeof(data_list[0]);i++)
                printf("%02X,",data_list[i]);
            data_list.clear();
            check = 0;
        }
        else{
            pos=(data_list[3]*256+data_list[4]+data_list[5]*256*256*256+data_list[6]*256*256);// 位置 
            data_list.clear();
        }


        vector<uint8_t> code2={0x03,0x0B,0x00,0x00,0x01};// 读取伸缩电机速度
        ser.write(CRC16_MudBus(code2,code2.size(),station_num));
        sleeptime_code.sleep();
        num=ser.available();
        if (num > 0) {
            size_t read_size = ser.read(data_list, num);
            if (read_size != num) {
                ROS_ERROR_STREAM("Failed to read all data from serial port.");
                return;
            }
        } 
        else {
            ROS_ERROR_STREAM("No data available on serial port.");
            return;
        }
        if (data_list[0]!=0x02 || data_list[1]!= 0x03){
            ROS_ERROR_STREAM("Receive wrong data list:");
            for(size_t i=0;i<sizeof(data_list)/sizeof(data_list[0]);i++)
                printf("%02X,",data_list[i]);
            data_list.clear();
            check = 0;
        }
        else{
            vel=data_list[3]*256+data_list[4];// 速度rpm
            data_list.clear();
        }


        vector<uint8_t> code3={0x03,0x0B,0x05,0x00,0x01};// 读取伸缩电机使能
        ser.write(CRC16_MudBus(code3,code3.size(),station_num));
        sleeptime_code.sleep();
        num=ser.available();
        if (num > 0) {
            size_t read_size = ser.read(data_list, num);
            if (read_size != num) {
                ROS_ERROR_STREAM("Failed to read all data from serial port.");
                return;
            }
        } 
        else {
            ROS_ERROR_STREAM("No data available on serial port.");
            return;
        }
        if (data_list[0]!=0x02 || data_list[1]!= 0x03){
            ROS_ERROR_STREAM("Receive wrong data list:");
            for(size_t i=0;i<sizeof(data_list)/sizeof(data_list[0]);i++)
                printf("%02X,",data_list[i]);
            data_list.clear();
            check = 0;
        }
        else{
            enable_state=data_list[4] % 2;// 使能状态,1使能,0未使能
            data_list.clear();
        }
        

        if(check){
            nh_.setParam("/read_arm_motor_enable_status", enable_state);// 设置伸缩电机使能状态参数
            nh_.setParam("/read_arm_motor_position", pos*0.1);// 设置伸缩电机位置参数 10 LSB -> 1 mm
            nh_.setParam("/read_arm_motor_speed", vel);// 设置伸缩电机速度参数
            cout<<"arm motor enable state="<<enable_state<<endl;
            cout<<"arm motor pos="<<pos*0.1<<endl;
            cout<<"arm motor vel="<<vel<<endl;
            cout<<"Read output successfully!"<<endl;
        }

    }
    return;
}

void serialpublisher::heartbeat_check()
{
    vector<uint8_t> data_list;
    bool check = true;
    // 俯仰电机心跳检测
    int station_num = 1;
    vector<uint8_t> code1={0x3E,0x08,0xB2,0x00,0x00,0x00,0x00,0x00,0x00,0x00};// 读取俯仰电机软件版本
    ser.write(CRC16_MudBus2(code1,code1.size(),station_num));
    
    sleeptime_code.sleep();
    int num=ser.available();

    // 1. 检查是否接收到数据
    if (num <= 0) {
        check = false;
    } else {
        // 读取数据
        size_t read_size = ser.read(data_list, num);
        if (read_size != num) {  // 检查读取是否完整
            check = false;
        } else {
            // 2. 检查数据长度是否足够
            if (data_list.size() < 13) {
                check = false;
            } else {
                // 3. 校验回复格式
                if (data_list[0] != 0x3E || data_list[1] != 0x01 || 
                    data_list[2] != 0x08 || data_list[3] != 0xB2 || 
                    data_list[4] != 0x00 || data_list[5] != 0x00 || 
                    data_list[6] != 0x00) {
                    check = false;
                } else {
                    // 4. CRC校验：取除最后2字节外的数据计算CRC，与最后2字节比较
                    vector<uint8_t> data_without_crc(data_list.begin(), data_list.end() - 2);
                    vector<uint8_t> calculated_crc = CRC16_MudBus3(data_without_crc, data_without_crc.size());

                    if (calculated_crc.size() < 13) {
                        check = false;
                    } else {
                        // 比较计算出的CRC与接收的CRC（最后两位）
                        if (calculated_crc[calculated_crc.size() - 2] != data_list[data_list.size() - 2] ||
                            calculated_crc[calculated_crc.size() - 1] != data_list[data_list.size() - 1]) {
                            check = false;
                        }
                    }
                }
            }
        }
    }
    
    // 5. 连续失败计数判断
    if (check) {
        pitch_motor_fail_count = 0;
        nh_.setParam("/pitch_motor_RS485_status", 1);
    } else {
        pitch_motor_fail_count++;
        // 连续失败3次处理
        if (pitch_motor_fail_count >= 3) {
            ROS_ERROR("俯仰电机通讯连续3次失败，判定为离线");
            nh_.setParam("/pitch_motor_RS485_status", 0);
        }
    }
    
    data_list.clear();  // 清理缓存
    check = true;  // 重置检查标志

    // 伸缩电机心跳检测
    station_num = 2;
    vector<uint8_t> code2={0x03,0x0B,0x00,0x00,0x01};// 读取伸缩电机速度
    ser.write(CRC16_MudBus(code2,code2.size(),station_num));
    sleeptime_code.sleep();
    num=ser.available();

    // 1. 检查是否接收到数据
    if (num <= 0) {
        check = false;
    } else {
        // 读取数据
        size_t read_size = ser.read(data_list, num);
        if (read_size != num) {  // 检查读取是否完整
            check = false;
        } else {
            // 2. 检查数据长度是否足够
            if (data_list.size() < 7) {
                check = false;
            } else {
                // 3. 校验回复格式
                if (data_list[0] != 0x02 || data_list[1] != 0x03 || 
                    data_list[2] != 0x02 ) {
                    check = false;
                } else {
                    // 4. CRC校验：取除最后2字节外的数据计算CRC，与最后2字节比较
                    vector<uint8_t> data_without_crc(data_list.begin(), data_list.end() - 2);
                    vector<uint8_t> calculated_crc = CRC16_MudBus3(data_without_crc, data_without_crc.size());

                    if (calculated_crc.size() < 7) {
                        check = false;
                    } else {
                        // 比较计算出的CRC与接收的CRC（最后两位）
                        if (calculated_crc[calculated_crc.size() - 2] != data_list[data_list.size() - 2] ||
                            calculated_crc[calculated_crc.size() - 1] != data_list[data_list.size() - 1]) {
                            check = false;
                        }
                    }
                }
            }
        }
    }
    
    // 5. 连续失败计数判断
    if (check) {
        arm_motor_fail_count = 0;
        nh_.setParam("/arm_motor_RS485_status", 1);
    } else {
        arm_motor_fail_count++;
        // 连续失败3次处理
        if (arm_motor_fail_count >= 3) {
            ROS_ERROR("伸缩电机通讯连续3次失败，判定为离线");
            nh_.setParam("/arm_motor_RS485_status", 0);
        }
    }
    
    return;
}


void serialpublisher::callback_sw(const liancheng_socket::SwitchOrder & order)
{
    uint8_t station_num=order.station_num;
    uint16_t switch_num=order.switch_num;
    uint8_t  case_num=order.case_num;
    this->switch_ch(station_num,switch_num,case_num);
    return;
}


vector<uint8_t> serialpublisher::CRC16_MudBus(vector<uint8_t> puchMsg, uint8_t usDataLen,uint8_t station_num){
	
	uint16_t uCRC = 0xffff;

    vector<uint8_t> code_v=puchMsg;
    code_v.insert(code_v.begin(),station_num);
    
    for(uint8_t num=0;num<usDataLen+1;num++)
    {
        cout<<int(code_v[num])<<endl;
    }
	
	for(uint8_t num=0;num<usDataLen+1;num++){
		uCRC = code_v[num]^uCRC;
		for(uint8_t x=0;x<8;x++){	
			if(uCRC&0x0001){	
				uCRC = uCRC>>1;	
				uCRC = uCRC^0xA001;	
			}else{	
				uCRC = uCRC>>1;	
			}
		}
	}
    code_v.push_back(uCRC&0x00ff);
    code_v.push_back(uCRC>>8);

	return code_v;

}

vector<uint8_t> serialpublisher::CRC16_MudBus2(vector<uint8_t> puchMsg, uint8_t usDataLen,uint8_t station_num){
	
	uint16_t uCRC = 0xffff;

    vector<uint8_t> code_v=puchMsg;
    code_v.insert(code_v.begin()+1,station_num);
	
	for(uint8_t num=0;num<usDataLen+1;num++){
		uCRC = code_v[num]^uCRC;
		for(uint8_t x=0;x<8;x++){	
			if(uCRC&0x0001){	
				uCRC = uCRC>>1;	
				uCRC = uCRC^0xA001;	
			}else{	
				uCRC = uCRC>>1;	
			}
		}
	}
    code_v.push_back(uCRC&0x00ff);
    code_v.push_back(uCRC>>8);

	return code_v;

}

vector<uint8_t> serialpublisher::CRC16_MudBus3(vector<uint8_t> puchMsg, uint8_t usDataLen){
	
	uint16_t uCRC = 0xffff;

    vector<uint8_t> code_v=puchMsg;
	
	for(uint8_t num=0;num<usDataLen+1;num++){
		uCRC = code_v[num]^uCRC;
		for(uint8_t x=0;x<8;x++){	
			if(uCRC&0x0001){	
				uCRC = uCRC>>1;	
				uCRC = uCRC^0xA001;	
			}else{	
				uCRC = uCRC>>1;	
			}
		}
	}
    code_v.push_back(uCRC&0x00ff);
    code_v.push_back(uCRC>>8);

	return code_v;

}
