# 라이브러리 import
import serial
import time

# --- 아두이노에 명령 전송하기 ---
def send_command(ser, command):
    """아두이노에 명령 전송"""
    if ser is not None and ser.is_open:
        ser.write(command.encode()) 
        return True
    return False   


# 아두이노 시리얼 연결 (COM 포트, 9600 속도)
try:
    ser = serial.Serial('COM4', 9600, timeout = 1)
    time.sleep(2) # 연결 안정화 대기
    print("✅ 아두이노 연결 성공!")
except Exception as e :
    print(f"❌ 아두이노 연결 실패: {e}")
    ser = None

# --- 기대값 확인 ---
result = send_command(ser, 'O')


if result:
    print("✅ PASS: 아두이노 명령 전송 성공!") # GREEN단계
else:
    print("❌ FAIL: send_command() 함수가 아직 구현되지 않았습니다") # RED단계

# 추가로 'C' 명령도 테스트
result = send_command(ser, 'C')

if result:
    print("✅ PASS: 문 닫기 명령 전송 성공!")
else:
    print("❌ FAIL: send_command() 함수가 아직 구현되지 않았습니다")

# 웹캠을 열기
# 색상 범위 설정 (과제 1에서 확인한 값)
# 이전 상태 변수 초기화

# 반복:
#   웹캠에서 프레임 읽기
#   HSV 색공간으로 변환
#   마스크 생성
#   마스크 픽셀 면적 계산
#   면적과 임계값 비교하여 상태 결정
#   상태가 이전 상태와 다르면 아두이노에 명령 전송
#   현재 상태를 화면에 표시
#   'q' 키 입력 시 루프 종료

# 리소스 해제