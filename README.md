# openus

## parser

### bill (법률안)
hwp 파일과 pdf 파일로 배포가 된다.
hwp 파일의 parsing이 어려워 한글(맥용 한컴오피스2014 VP사용)으로 파일을 열어 다른이름으로 저장(.docx)로 워드로 변형한 뒤 "python-docx"라이브러리를 이용해 파싱한다.

