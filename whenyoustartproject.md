# 💳 Don-worry: 프로젝트 통합 시작 가이드

본 문서는 **Don-worry** 프로젝트의 초기 세팅, 실행 방법 및 협업 규칙을 담고 있습니다.  
팀원분들은 원활한 개발을 위해 아래 가이드를 반드시 숙지해 주세요.

---

## 📂 1. 프로젝트 구조 (Project Structure)

우리 프로젝트는 **모노레포(Monorepo)** 스타일로 관리됩니다.
```text
donworry-project/           # 최상위 루트 (Git Init 위치)
├── donworry-frontend/      # Vue.js 프로젝트 (Vite + Tailwind v4)
├── donworry-backend/         # Django 프로젝트 (DRF + Kafka 연동)
└── whenyoustartpjt.md      # 바로 이 가이드 파일!

```

---

## 🐍 2. 백엔드 세팅 (Django & Kafka)

가상환경(venv) 사용을 **적극 권장**합니다. 환경에 맞춰 아래 명령어를 실행하세요.

### 💡 가상환경 생성 및 활성화

```bash
cd donworry-backend

# 가상환경 생성 (최초 1회)
python -m venv venv

# 가상환경 활성화 (Windows)
source venv/Scripts/activate

# 가상환경 활성화 (Mac/Linux)
source venv/bin/activate

```

### 📦 패키지 설치 및 DB 초기화 (Migration)

가상환경이 활성화된 상태에서 진행하세요.

```bash
# 필수 패키지 설치
pip install -r requirements.txt

# 데이터베이스 마이그레이션 (필수)
python manage.py makemigrations
python manage.py migrate

```

---

## 🎨 3. 프론트엔드 세팅 (Vue.js)

우리 프로젝트는 **Tailwind CSS v4**와 **Chart.js**를 사용합니다.

```bash
cd donworry-frontend

# 의존성 설치 (최초 1회)
npm install

# 로컬 개발 서버 실행
npm run dev

```

---

## 🚀 4. 서버 실행 및 주요 경로

| 구분 | 실행 경로 | 명령어 | 접속 주소 |
| --- | --- | --- | --- |
| **Backend** | `/donworry-backend` | `python manage.py runserver` | `http://localhost:8000` |
| **Frontend** | `/donworry-frontend` | `npm run dev` | `http://localhost:5173` |

### 📥 금융 상품 데이터 수집 (Save API)

서버를 처음 실행한 후, 아래 경로에 접속하여 금융감독원 데이터를 DB에 저장해야 합니다.

* **경로:** `http://localhost:8000/api/products/save/`
* **조건:** `.env` 파일에 유효한 `FINLIFE_API_KEY`가 있어야 합니다.

---

---

## 😎 5. CI/CD 자동화 가이드 (`deploy.yml`)

이 파일은 **GitHub Actions**를 사용하여 로컬에서 `push`한 코드를 **AWS EC2 서버에 자동으로 배포**하는 스크립트입니다.

### 5-1. 작동 원리 (Workflow)

1. **Trigger:** `master` 브랜치에 코드가 `push`되면 작업 시작.
2. **Runner:** GitHub에서 제공하는 가상 우분투 환경(`ubuntu-latest`)에서 실행.
3. **Action:** `appleboy/ssh-action`을 사용하여 우리 EC2 서버에 SSH로 원격 접속.
4. **Execution:** 서버 터미널에서 우리가 작성한 명령어를 순차적으로 실행.

---

### 5-2. 주요 설정 항목 (Secrets)

보안을 위해 민감한 정보는 GitHub 레포지토리의 **Settings > Secrets > Actions**에 미리 등록해야 합니다.

* **`EC2_HOST`**: 서버의 퍼블릭 IP 주소 (`15.165.238.176`)
* **`EC2_USERNAME`**: 접속 계정 이름 (주로 `ubuntu`)
* **`EC2_SSH_KEY`**: 서버 접속용 `.pem` 키 파일의 전체 내용

---

### 5-3. 단계별 명령어 설명

| 단계 | 명령어 | 역할 |
| --- | --- | --- |
| **코드 동기화** | `git fetch --all` / `reset --hard` | 서버의 코드를 깃허브 최신 상태와 강제로 일치시킴 |
| **백엔드 이동** | `cd donworry-backend` | Django 프로젝트 폴더로 진입 |
| **가상환경** | `python3 -m venv venv` | 독립적인 패키지 실행 환경 구축 (최초 1회) |
| **라이브러리** | `pip install -r requirements.txt` | `backend` 운영에 필요한 파이썬 패키지들 설치 |
| **DB 반영** | `python manage.py migrate` | 변경된 데이터베이스 모델(Model) 구조를 DB에 적용 |
| **프론트 이동** | `cd ../donworry-frontend` | Vue.js 프로젝트 폴더로 이동 |
| **의존성 설치** | `npm install` | Vue 프로젝트에 필요한 Node.js 라이브러리 설치 |
| **빌드(Build)** | `npm run build` | **핵심:** 작성한 코드를 브라우저가 읽을 수 있는 정적 파일(`dist`)로 구워냄 |

---

### 💡 주의사항 (Troubleshooting)

* **폴더명 불일치:** 서버에 생성된 실제 폴더명과 `deploy.yml`의 `cd` 경로가 다르면 배포가 중단됩니다.
* **권한 문제:** `npm install`이나 `build` 도중 권한 에러가 발생하면 서버에서 해당 폴더의 소유권(`chown`)을 확인해야 합니다.
* **메모리 부족:** `t2.micro` 사양에서 Vue 빌드 시 멈춤 현상이 발생할 수 있으므로, 반드시 Swap Memory(2GB 이상)가 설정되어 있어야 합니다.

---


## ⚠️ 6. 협업 유의사항 (Precaution)

### 🔐 보안 (Secret Keys)

* **`.env` 파일은 절대 Push 하지 마세요.** - `.env.example` 파일을 복사하여 본인의 API 키를 입력한 뒤 `.env`로 이름을 바꿔서 사용하세요.

### 🌿 Git 관리 규칙

* **최상위 폴더에서만 `git init`을 관리합니다.**
* 혹시 하위 폴더(`donworry-frontend`, `donworry-backend`) 내부에 `.git` 폴더가 있다면 반드시 삭제 후 최상위에서 커밋해 주세요.
* **절대 커밋 금지:** `node_modules/`, `venv/`, `db.sqlite3`, `.env`

### 🛠 기술 스택 특이사항

* **CSS:** Tailwind v4 방식에 따라 `src/assets/main.css`에는 `@import "tailwindcss";` 한 줄만 포함됩니다.
* **API 요청:** 프론트에서 백엔드로 요청 시 `axios`를 사용하며, CORS 에러 발생 시 백엔드 `settings.py` 설정을 확인하세요.

---



> **Tip:** 코드를 새로 내려받은 경우, 반드시 `pip install`과 `npm install`을 다시 실행하여 라이브러리 버전을 맞춰주세요!

---

