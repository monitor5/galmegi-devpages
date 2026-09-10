<div align="center">

<img src="assets/gull.svg" width="72" height="72" alt="갈매기개발단">

# 갈매기개발단

**작은 불편함에서, 새로운 비행으로.**

일상에서 발견한 문제를 코드로 풀어가는 사람들과 우리가 만든 서비스를 소개합니다.

[웹사이트 방문 ↗](https://dev.galmegi.com) · [여행갈매기 ↗](https://galmegi.com) · [이메일](mailto:galgalmegi@gmail.com)

---

</div>

## 생각을 서비스로

**여행갈매기**는 부산 여행의 일정, 이동, 짐 정보, 친구와의 만남을 하나의 흐름으로 연결합니다. 이 저장소는 여행갈매기와 개발진을 소개하는 개발단 웹사이트의 소스입니다.

흰색과 검정 중심의 화면, 각 개발진의 GitHub 프로필 사진, 명확한 글자와 여백으로 내용을 담았습니다. 데스크톱부터 모바일까지 화면 크기에 따라 레이아웃이 달라집니다.

## 함께 만드는 사람들

| 이름 | GitHub |
| :--- | :--- |
| 김우현 | [@monitor5](https://github.com/monitor5) |
| 하건우 | [@hardtack-dev](https://github.com/hardtack-dev) |
| 김예람 | [@kyr040404](https://github.com/kyr040404) |
| 권창빈 | [@k1changbin](https://github.com/k1changbin) |

## 가볍게 실행하기

HTML과 CSS로 구성되어 패키지 설치나 빌드가 필요하지 않습니다. Python 3가 있다면 아래 명령으로 확인할 수 있습니다.

```sh
git clone https://github.com/monitor5/galmegi-devpages.git
cd galmegi-devpages
python3 -m http.server 4180 --bind 127.0.0.1
```

브라우저에서 [localhost:4180](http://localhost:4180)을 엽니다.

## 소스 안내

```text
├── index.html       서비스·개발진 소개, 프로필·이메일 링크
├── style.css        흑백 테마, 반응형 레이아웃
├── assets/          갈매기 아이콘, 서비스 로고와 화면
├── robots.txt       검색 크롤러 안내
└── sitemap.xml      공개 페이지 주소
```

콘텐츠는 `index.html`, 디자인은 `style.css`에서 수정합니다. CSS 변경 시 HTML의 `style.css?v=...` 값도 바꾸면 기존 방문자의 캐시와 충돌을 피할 수 있습니다. 프로필 사진은 저장소에 포함해 외부 이미지 장애나 변경에 영향을 받지 않습니다.

키보드 포커스, 본문 바로가기, 새 탭 안내와 동작 줄이기 설정을 지원합니다. 이메일은 `galgalmegi@gmail.com` 그대로 표시하며, 클릭하면 메일 앱을 엽니다.

## 배포

[dev.galmegi.com](https://dev.galmegi.com)은 기존 서버의 Nginx에서 정적 파일로 제공합니다. GitHub Pages는 사용하지 않습니다. 데이터베이스나 별도 애플리케이션 프로세스가 필요하지 않습니다.

배포할 파일은 `index.html`, `style.css`, `robots.txt`, `sitemap.xml`, `assets/`입니다. 서버의 새 릴리스 디렉터리에 이 파일만 복사하고 활성 심볼릭 링크를 교체합니다. 이전 릴리스로 링크를 되돌려 복구할 수 있습니다. 콘텐츠 수정에는 Nginx 재시작이 필요하지 않습니다.

`main`에 push하면 **GitHub Actions → 검증 → 배포 → HTTPS 확인**이 자동 실행됩니다. PR에서는 검증만 실행합니다. Actions의 `Run workflow`로 수동 실행할 수도 있습니다.

- HTML 자산 경로·앵커·아이콘 크기·XML을 먼저 검사합니다.
- 배포 전용 SSH 키는 GitHub Secrets에 저장합니다. 서버 계정은 sudo 권한이 없고, 강제 명령으로 정적 파일 배포만 허용합니다.
- 허용한 공개 파일만 패키징하고 새 릴리스로 전환합니다. 서버 검증 실패 시 이전 릴리스로 복구합니다.
- 마지막으로 공개 HTTPS의 `revision.txt`가 이번 커밋과 실행 번호인지 확인합니다. 공개망 검증 실패는 Actions 실패로 표시되며 서버의 정상 릴리스는 유지합니다.
- 같은 브랜치의 배포는 순서대로 처리합니다. 기존 앱 프로세스는 재시작하지 않습니다.

[배포 실행 기록](https://github.com/monitor5/galmegi-devpages/actions/workflows/deploy.yml)

설정 Secrets: `DEPLOY_HOST`, `DEPLOY_USER`, `DEPLOY_SSH_KEY`, `DEPLOY_KNOWN_HOSTS`. 수신 프로그램은 `ops/receive-deploy.py`이며 서버의 root 소유 경로에 설치합니다. 이 프로그램 자체의 변경은 별도 서버 설치가 필요합니다. 접속키는 저장소에 포함하지 않습니다.

## 이용 및 문의

문의: **[galgalmegi@gmail.com](mailto:galgalmegi@gmail.com)**

라이선스는 아직 지정하지 않았습니다. 서비스 이미지와 로고의 재사용은 개발단에 문의해 주세요.

---

<div align="center">갈매기개발단 · 직접 만들고, 써보고, 더 나아지게.</div>
