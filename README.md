# imizi_api
> Fastcampus 이태훈 강사님의 FastAPI 강의 수강 후 진행하는 클론 코딩

### 이미지를 저장해 주고 서빙하는 API 서버
- imgbb 와 같은 서비스
- 이미지를 대신 저장
- Global CDN 서비스
- 이미지 조회, 삭제, 저장 기능
- PNG, JPG 등을 webp로 변환
  - webp는 차세대 포멧. 더 적은 용량으로 같은 퀄리티의 이미지 서빙 가능

### 시스템 구조
- 유저가 이미지를 저장하고, 저장된 이미지의 url을 서버로 요청
- FastAPI 서버는 유저에게 이미지 저장 경로를 제공
- 유저가 이미지 저장 경로를 접속하면 클라우드 프론트로부터 서빙을 받음