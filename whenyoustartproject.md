# 💳 Don-worry: 프로젝트 통합 시작 가이드

본 문서는 **Don-worry** 프로젝트의 초기 세팅, 실행 방법 및 협업 규칙을 담고 있습니다.  
팀원분들은 원활한 개발을 위해 아래 가이드를 반드시 숙지해 주세요.

---

## 📂 1. 프로젝트 구조 (Project Structure)

우리 프로젝트는 **모노레포(Monorepo)** 스타일로 관리됩니다.
```text
donworry-project/           # 최상위 루트 (Git Init 위치)
├── donworry-frontend/      # Vue.js 프로젝트 (Vite + Tailwind v4)
├── donworry-kafka/         # Django 프로젝트 (DRF + Kafka 연동)
└── whenyoustartpjt.md      # 바로 이 가이드 파일!

```

---

## 🐍 2. 백엔드 세팅 (Django & Kafka)

가상환경(venv) 사용을 **적극 권장**합니다. 환경에 맞춰 아래 명령어를 실행하세요.

### 💡 가상환경 생성 및 활성화

```bash
cd donworry-kafka

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
| **Backend** | `/donworry-kafka` | `python manage.py runserver` | `http://localhost:8000` |
| **Frontend** | `/donworry-frontend` | `npm run dev` | `http://localhost:5173` |

### 📥 금융 상품 데이터 수집 (Save API)

서버를 처음 실행한 후, 아래 경로에 접속하여 금융감독원 데이터를 DB에 저장해야 합니다.

* **경로:** `http://localhost:8000/api/products/save/`
* **조건:** `.env` 파일에 유효한 `FINLIFE_API_KEY`가 있어야 합니다.

---

## ⚠️ 5. 협업 유의사항 (Precaution)

### 🔐 보안 (Secret Keys)

* **`.env` 파일은 절대 Push 하지 마세요.** - `.env.example` 파일을 복사하여 본인의 API 키를 입력한 뒤 `.env`로 이름을 바꿔서 사용하세요.

### 🌿 Git 관리 규칙

* **최상위 폴더에서만 `git init`을 관리합니다.**
* 혹시 하위 폴더(`frontend`, `kafka`) 내부에 `.git` 폴더가 있다면 반드시 삭제 후 최상위에서 커밋해 주세요.
* **절대 커밋 금지:** `node_modules/`, `venv/`, `db.sqlite3`, `.env`

### 🛠 기술 스택 특이사항

* **CSS:** Tailwind v4 방식에 따라 `src/assets/main.css`에는 `@import "tailwindcss";` 한 줄만 포함됩니다.
* **API 요청:** 프론트에서 백엔드로 요청 시 `axios`를 사용하며, CORS 에러 발생 시 백엔드 `settings.py` 설정을 확인하세요.

---



> **Tip:** 코드를 새로 내려받은 경우, 반드시 `pip install`과 `npm install`을 다시 실행하여 라이브러리 버전을 맞춰주세요!

---

