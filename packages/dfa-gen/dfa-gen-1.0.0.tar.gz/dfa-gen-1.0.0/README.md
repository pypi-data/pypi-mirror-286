## DFA-generator
_A python package generating DFA and its graph from protein sequence (and UTR sequence as an option)_

### 1. description

- protein sequence와 utr을 입력하면 [LinearDesign](https://github.com/LinearDesignSoftware/LinearDesign)에서 사용할 수 있는 DFA를 생성하고 이를 시각화한 graph를 생성합니다.
- 본 package로 만들어진 DFA는 <U>수정된 LinearDesign 프로그램에서만</U> 사용할 수 있습니다. (WIP)
- graph 예시 이미지 (`dfa-gen "MA" -l 3 -u UGGACGA`의 결과)
  - `green node`: protein sequence
  - `blue node`: 3'UTR sequence
  - `red node`: stop codon or last node
  
  ![dfa_MA_graph](https://github.com/user-attachments/assets/ebf9782f-fdd3-48e3-9c43-2d2451b283ef)

### 2. pre-requirement
1. `python`
2. `pandas`
3. `graphviz`

### 3. to run

- root에서 다음의 명령어를 먼저 실행해주세요. (root =`setup.py`가 있는 위치)

  ```
  pip install .
  ```
- 이후에는 root에서 다음의 명령어와 옵션으로 실행가능합니다.
  
  ```
  dfa-gen [PROTEIN_SEQUENCE] [OPTIONS]
  ```
- 이미지를 포함한 결과 파일들은 `./result` 디렉토리에 저장됩니다.
  
### 4. options
  1.  `--utr` 옵션을 사용하면 nucleotide sequence를 넘겨줄 수 있습니다. (default: empty string)
     
      ```
      --utr [UTR_SEQUENCE] or -u [UTR_SEQUENCE]
      ```
  3.  `--lambda` 옵션을 사용하면 가중치 계산에 사용될 lambda 값을 지정할 수 있습니다. (default: 0)
     
      ```
      --lambda_val [LAMBDA] or -l [LAMBDA]
      ``` 
- example
  
  ```
  dfa-gen METFWPLPAW -u UGGACGA
  dfa-gen "MEFA" -l 3 -u UGGACGA
  ```
