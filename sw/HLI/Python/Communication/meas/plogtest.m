clear
load plog.txt;
imu_o = plog(:,2);
gps_o = plog(:,3);
imu = plog(find(imu_o),[1 2]);
gps = plog(find(gps_o),[1 3]);
gps_n = 1;
gps_m = [];
gps_r = [];
clc
for i = 2:numel(gps)
    if(gps(i,2) - gps(i-1,2) ~= 1 && gps(i,2) ~= 1 && gps(i-1,2)~=255 && gps(i,2) ~= 0 && gps(i-1,2)~=0)% && gps(i,2) - gps(i-1,2) ~= 0)
        gps_m(gps_n) = i;
        gps_r(gps_n) = (gps(i,2) - gps(i-1,2));
        gps_n = gps_n + 1;
    end
end

imu_n = 1;
imu_m = [];
imu_r = [];
clc
for i = 2:numel(imu)
    if(imu(i,2) - imu(i-1,2) ~= 1 && imu(i,2) ~= 1 && imu(i-1,2)~=255 && imu(i,2) ~= 0 && imu(i-1,2)~=0)% && imu(i,2) - imu(i-1,2) ~= 0)
        imu_m(imu_n) = i;
        imu_r(imu_n) = (imu(i,2) - imu(i-1,2));
        imu_n = imu_n + 1;
    end
end

[imu_m',[0,diff(imu_m)]',imu(imu_m),imu(imu_m-1),imu(imu_m)-imu(imu_m-1)]
[gps(gps_m),gps(gps_m-1),gps(gps_m)-gps(gps_m-1)]'
sum((imu(imu_m)-imu(imu_m-1)-1))
p_imu = 100*sum((imu(imu_m)-imu(imu_m-1)-1))/numel(imu)
p_gps = 100*sum((gps(gps_m)-gps(gps_m-1)-1))/numel(gps)