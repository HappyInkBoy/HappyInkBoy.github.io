/* Fun with C
 * See https://www.youtube.com/watch?v=rSsYr1gU_A4 for my VS Code setup on Mac ( C/C++ extension and Runner extension )
 * and https://c-faq.com/aryptr/dynmuldimary.html for multi-dimensional array. We use the simplest approach
 * int *array3 = malloc(nrows * ncolumns * sizeof(int));
 */


#include <stdio.h>
#include <stdlib.h>

int* add(int *m1, int *m2) {
  int *m3 = malloc(3 * 3 * sizeof(int));
  int i;
  for (i=0; i<9; i++) {
    m3[i] = m1[i] + m2[i];
  }
  return m3;
}

void print(int *m) {
  printf("%d %d %d\r\n", m[0], m[1], m[2]);
  printf("%d %d %d\r\n", m[3], m[4], m[5]);
  printf("%d %d %d\r\n", m[6], m[7], m[8]);
}

int main() {
  printf("Ok");
  int a=sizeof(int);
  int *m1 = malloc(3 * 3 * sizeof(int));
  int i;
  int count = 0;
  for (i=0; i < 3; i++) {
    int j;
    for (j=0; j < 3; j++) {
      m1[3*j+i] = count;
      count++;
    }
  }
  print(m1);
  int *m2 = malloc(3 * 3 * sizeof(int));
  for (i=0; i < 3; i++) {
    int j;
    for (j=0; j < 3; j++) {
      m2[3*j+i] = 10*count;
      count++;
    }
  }
  print(m2);

  int* placeholder = add(m1,m2);
  print(placeholder);

  free(m1);
  free(m2);
  free(placeholder);
  return 0;
}
