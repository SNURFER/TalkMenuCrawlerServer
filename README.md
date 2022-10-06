# 티맥스밥봇 스킬서버 개발
* 카카오 채널명 : 티맥스밥봇
## 스킬서버 구성
* nodejs express 서버
  * 챗봇 발화에 대한 message 핸들링 처리
  * schedule job을 정의하여 매주 특정 날짜에 식당 메뉴를 파싱하도록 함
* 파이썬 모듈을 사용
  * 셀레니움을 통한 웹크롤링
  * pandas 이용 xlsx 메뉴 파서 구현
### 서버 구동 방법
```
vim input (id, pw 설정)
npm install
npm run serve
```

## 카카오 오픈빌더와 연동하여 챗봇 서비스 제공
<img width="383" alt="스크린샷 2022-10-06 오전 11 50 31" src="https://user-images.githubusercontent.com/42398891/194207086-57ef48b0-201e-4bfd-b7e3-4be23a51a303.png">
<img width="398" alt="스크린샷 2022-08-04 오후 11 51 58" src="https://user-images.githubusercontent.com/42398891/182877979-e8fa53eb-32ee-4db0-898e-ce5f45dcf809.png">
