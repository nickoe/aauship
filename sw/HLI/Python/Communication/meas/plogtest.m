clear
load plog.txt;
imu_o = plog(:,1);
gps_o = plog(:,2);
imu = imu_o(find(imu_o));
gps = gps_o(find(gps_o));
gps_n = 1;
gps_m = [];
gps_r = [];
clc
for i = 2:numel(gps)
    if(gps(i) - gps(i-1) ~= 1 && gps(i) ~= 1 && gps(i-1)~=255 && gps(i) ~= 0 && gps(i-1)~=0 && gps(i) - gps(i-1) ~= 0)
        gps_m(gps_n) = i;
        gps_r(gps_n) = (gps(i) - gps(i-1));
        gps_n = gps_n + 1;
    end
end

imu_n = 1;
imu_m = [];
imu_r = [];
clc
for i = 2:numel(imu)
    if(imu(i) - imu(i-1) ~= 1 && imu(i) ~= 1 && imu(i-1)~=255 && imu(i) ~= 0 && imu(i-1)~=0 && imu(i) - imu(i-1) ~= 0)
        imu_m(imu_n) = i;
        imu_r(imu_n) = (imu(i) - imu(i-1));
        imu_n = imu_n + 1;
    end
end

[imu_m',[0,diff(imu_m)]',imu(imu_m),imu(imu_m-1),imu(imu_m)-imu(imu_m-1)]
[gps(gps_m),gps(gps_m-1),gps(gps_m)-gps(gps_m-1)]'
sum((imu(imu_m)-imu(imu_m-1)-1))
p_imu = 100*sum((imu(imu_m)-imu(imu_m-1)-1))/numel(imu)
p_gps = 100*sum((gps(gps_m)-gps(gps_m-1)-1))/numel(gps)