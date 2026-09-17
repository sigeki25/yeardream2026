# mariadb 설치
sudo yum install -y mariadb1011-server mariadb1011

# mariadb 실행
sudo systemctl start mariadb

# 서비스 등록(서버가 켜지면 무조건 같이 켜지도록)
sudo systemctl enable mariadb

# 상태 확인
sudo systemctl status mariadb

# 관리자(root) 계정 설정
sudo mysql_secure_installation
# Switch to unix_socket authentication:n # 비번 없이 DB 접속 여부
# Change the root password?:n # 비번 변경 여부
# Remove anonymous users?:Y # 익명유저 삭제여부
# Disallow root login remotely? Y (원격 root 접속 제한)
# Remove test database and access to it? Y (테스트 DB 삭제)
# Reload privilege tables now? Y (권한 적용)

# 관리자(root)로 접속 해보기
sudo mysql -u root -p

# USER 생성
# CREATE USER [ID]@[접속IP] IDENTIFIED BY [PASSWORD];
CREATE USER 'web_user'@'%' IDENTIFIED BY 'user@pass';

# 확인
SELECT Host, User, Password FROM mysql.user;

# 권한 생성
# GRANT [권한 종류] ON [어디에서 사용할 수 있는지] TO [대상];
GRANT ALL PRIVILEGES ON *.* TO 'web_user'@'%';
