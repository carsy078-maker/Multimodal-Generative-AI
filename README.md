# Multimodal Generative AI Asset Automation Pipeline

본 프로젝트는 고품질 이미지 및 비디오 에셋의 일관성 있는 생성을 위해 **ComfyUI** 노드 기반으로 설계된 자동화 파이프라인입니다. 특히 8GB VRAM이라는 제한된 환경에서 14B급 대규모 모델을 안정적으로 구동하기 위한 **메모리 최적화 엔지니어링**에 초점을 맞추었습니다.

## 핵심 기능

- **이미지-비디오 통합 워크플로우:** SDXL/Flux로 생성된 고해상도 이미지를 LTX-Video 및 WAN 모델과 연계하여 자연스러운 비디오로 변환하는 연속 추론 파이프라인을 구축했습니다.
- **VLM 기반 지능형 피드백:** Qwen(Vision Language Model)을 파이프라인에 통합하여 생성된 에셋을 분석하고, 그 결과를 바탕으로 프롬프트를 자동 보정하는 폐쇄 루프(Closed-loop) 시스템을 구현했습니다.
- **노드 기반 자동화:** 복잡한 생성 과정을 개별 노드로 모듈화하여 유지보수성을 높이고, 반복적인 작업 없이 대량의 에셋을 생성할 수 있도록 워크플로우를 최적화했습니다.

## 기술 스택

- **AI Engine:** ComfyUI
- **Generative Models:** Flux.1, SDXL, WAN (14B), LTX-Video
- **Vision Language Model:** Qwen-VL
- **Hardware Context:** NVIDIA RTX 3070 (8GB VRAM)
- **Format:** API JSON Workflow, Python

## 디렉터리 구조 (Directory Structure)

- `workflows/`: ComfyUI 워크플로우 JSON 파일 저장
- `scripts/`: ComfyUI API와 상호작용하는 파이썬 스크립트 저장 (예: `workflow_api_runner.py`)
- `assets/`: 워크플로우에서 사용되는 이미지, 비디오 등 에셋 저장

## 시스템 아키텍처

1.  **Prompt Entry:** 사용자 정의 텍스트 입력 및 조건 설정
2.  **Image Generation:** Flux/SDXL 모델을 통한 고품질 베이스 이미지 생성
3.  **VLM Analysis:** Qwen 모델이 이미지를 분석하여 묘사 및 품질 검수 수행
4.  **Auto-Correction:** 분석 결과를 바탕으로 프롬프트를 재작성하여 이미지 품질 보정
5.  **Video Synthesis:** WAN/LTX-Video 모델을 통한 동적 비디오 변환 및 업스케일링

---

## 기술적 도전 및 최적화

### 1. 8GB VRAM 환경에서의 대규모 모델(14B) 구동 최적화
- **문제 사항:** WAN(14B)과 같은 대규모 비디오 모델 구동 시 VRAM 부족으로 인한 OOM(Out of Memory) 및 시스템 스와핑 발생으로 생성 속도가 급격히 저하되었습니다.
- **해결 방안:** - **Int8 Quantization:** 가중치를 Int8 형식으로 양자화하여 모델의 메모리 점유율을 50% 이상 절감했습니다.
    - **Spatial Tiling:** 전체 프레임을 한 번에 연산하지 않고 구획별로 나누어 처리하는 타일링 기법을 적용하여 피크 메모리 사용량을 8GB 이내로 통제했습니다.
- **성과:** 하드웨어 업그레이드 없이 소프트웨어 최적화만으로 안정적인 비디오 추론 환경을 확보했습니다.

### 2. 메모리 관리 효율화
- **해결 방안:** 노드 실행 전후로 불필요한 모델 가중치를 VRAM에서 즉시 해제하는 **메모리 스케줄링**을 적용하여 연속적인 멀티 모델 구동 환경을 안정화했습니다.

---

## 실행 가이드

<Steps>
{/* Reason: ComfyUI 워크플로우는 설치 순서와 모델 배치가 틀리면 실행되지 않으므로 순서가 매우 중요합니다. */}
  <Step title="ComfyUI 환경 구성" subtitle="의존성 설치">
    로컬 환경에 ComfyUI를 설치하고 필수 패키지를 설치합니다.
    ```bash
    pip install -r requirements.txt
    ```
    이후 필수 커스텀 노드(Manager, VideoHelperSuite 등)를 설치합니다.
  </Step>
  <Step title="모델 체크포인트 배치" subtitle="models 폴더">
    `Flux`, `WAN`, `Qwen` 등 사용되는 모델 가중치 파일들을 지정된 경로에 배치합니다. (양자화 버전 권장)
  </Step>
  <Step title="서버 실행 및 워크플로우 로드" subtitle="JSON Import">
    ComfyUI 서버를 로컬에서 실행합니다 (기본값: `http://127.0.0.1:8188`).
    `workflows/` 폴더 내의 API JSON 파일을 ComfyUI 화면에 드래그하여 로드하거나 API를 통해 실행할 수 있습니다.
  </Step>
  <Step title="파이프라인 실행" subtitle="Queue Prompt">
    프롬프트를 입력하고 'Queue Prompt'를 누르거나 파이썬 스크립트를 통해 자동화된 프로세스를 시작합니다.
    ```bash
    python scripts/workflow_api_runner.py
    ```
  </Step>
</Steps>

---

> **Note:** 본 프로젝트의 모든 워크플로우는 API 호출이 가능한 JSON 포맷으로 저장되어 있어, FastAPI 등 외부 백엔드 서버와의 연동이 용이합니다.
