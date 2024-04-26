undefined8 main(void)
{
  char *pcVar1;
  undefined *puVar2;
  int iVar3;
  ushort **ppuVar4;
  undefined8 uVar5;
  char *pcVar6;
  undefined *puVar7;
  long in_FS_OFFSET;
  char cStack_168d8;
  char cStack_168d7;
  int iStack_168d4;
  int iStack_168d0;
  int iStack_168cc;
  int iStack_168c8;
  int iStack_168c4;
  int iStack_168c0;
  int iStack_168bc;
  int iStack_168b8;
  int iStack_168b4;
  int iStack_168b0;
  char *pcStack_168a8;
  char *pcStack_168a0;
  char *apcStack_16878 [270];
  undefined auStack_16008 [28592];
  char *local_f058 [3844];
  char *local_7838 [3845];
  long canary;
  
  puVar2 = &stack0xfffffffffffffff8;
  do {
    puVar7 = puVar2;
    *(undefined8 *)(puVar7 + -0x1000) = *(undefined8 *)(puVar7 + -0x1000);
    puVar2 = puVar7 + -0x1000;
  } while (puVar7 + -0x1000 != auStack_16008);
  canary = *(long *)(in_FS_OFFSET + 0x28);



  iStack_168d4 = 0;
  for (cStack_168d8 = '0'; cStack_168d8 < '{'; cStack_168d8 = cStack_168d8 + '\x01') {
    *(undefined8 *)(puVar7 + -0x18d8) = 0x1021bc;
    ppuVar4 = __ctype_b_loc();
    if (((*ppuVar4)[cStack_168d8] & 8) != 0) {
      *(undefined8 *)(puVar7 + -0x18d8) = 0x1021e9;
      pcVar6 = (char *)calloc(2,1);
      apcStack_16878[iStack_168d4] = pcVar6;
      pcVar6 = apcStack_16878[iStack_168d4];
      *(undefined8 *)(puVar7 + -0x18d8) = 0x102233;
      sprintf(pcVar6,"%c",(ulong)(uint)(int)cStack_168d8);
      iStack_168d4 = iStack_168d4 + 1;
    }
  }
  iStack_168d4 = 0x3e;
  for (iStack_168d0 = 0; iStack_168d0 < 0x3e; iStack_168d0 = iStack_168d0 + 1) {
    *(undefined8 *)(puVar7 + -0x18d8) = 0x102278;
    pcVar6 = (char *)calloc(2,1);
    apcStack_16878[iStack_168d4] = pcVar6;
    pcVar6 = apcStack_16878[iStack_168d4];
    *(undefined8 *)(puVar7 + -0x18d8) = 0x1022b9;
    sprintf(pcVar6,"%s",&DAT_0010300c);
    pcVar6 = apcStack_16878[iStack_168d0];
    pcVar1 = apcStack_16878[iStack_168d4];
    *(undefined8 *)(puVar7 + -0x18d8) = 0x1022e4;
    strcat(pcVar1,pcVar6);
    iStack_168d4 = iStack_168d4 + 1;
  }
  for (iStack_168cc = 0; iStack_168cc < 0x3e; iStack_168cc = iStack_168cc + 1) {
    for (iStack_168c8 = 0; iStack_168c8 < 0x3e; iStack_168c8 = iStack_168c8 + 1) {
      *(undefined8 *)(puVar7 + -0x18d8) = 0x10232c;
      pcVar6 = (char *)calloc(2,1);
      local_f058[(long)iStack_168cc * 0x3e + (long)iStack_168c8] = pcVar6;
      local_f058[(long)iStack_168cc * 0x3e + (long)iStack_168c8] =
           apcStack_16878[iStack_168cc + iStack_168c8];
    }
  }
  iStack_168d4 = 0x7c;
  iStack_168c4 = 2;
  for (cStack_168d7 = '2'; cStack_168d7 < '{'; cStack_168d7 = cStack_168d7 + '\x01') {
    *(undefined8 *)(puVar7 + -0x18d8) = 0x1023e8;
    ppuVar4 = __ctype_b_loc();
    if (((*ppuVar4)[cStack_168d7] & 8) != 0) {
      for (iStack_168c0 = 0; iStack_168c0 < 0x3e; iStack_168c0 = iStack_168c0 + 1) {
        *(undefined8 *)(puVar7 + -0x18d8) = 0x102428;
        pcVar6 = (char *)calloc(2,1);
        apcStack_16878[iStack_168d4] = pcVar6;
        pcVar6 = apcStack_16878[iStack_168d4];
        *(undefined8 *)(puVar7 + -0x18d8) = 0x102469;
        sprintf(pcVar6,"%c",(ulong)(uint)(int)cStack_168d7);
        pcVar6 = apcStack_16878[iStack_168d4 + iStack_168c4 * -0x3e];
        pcVar1 = apcStack_16878[iStack_168d4];
        *(undefined8 *)(puVar7 + -0x18d8) = 0x1024a7;
        strcat(pcVar1,pcVar6);
        iStack_168d4 = iStack_168d4 + 1;
      }
      iStack_168c4 = iStack_168c4 + 1;
    }
  }
  for (iStack_168bc = 0; iStack_168bc < 0x3e; iStack_168bc = iStack_168bc + 1) {
    for (iStack_168b8 = 0; iStack_168b8 < 0x3e; iStack_168b8 = iStack_168b8 + 1) {
      *(undefined8 *)(puVar7 + -0x18d8) = 0x102513;
      pcVar6 = (char *)calloc(2,1);
      local_7838[(long)iStack_168bc * 0x3e + (long)iStack_168b8] = pcVar6;
      if (iStack_168bc == 0) {
        local_7838[iStack_168b8] = "0";
      }
      else if (iStack_168bc == 1) {
        local_7838[(long)iStack_168b8 + 0x3e] = apcStack_16878[iStack_168b8];
      }
      else {
        local_7838[(long)iStack_168bc * 0x3e + (long)iStack_168b8] =
             apcStack_16878[iStack_168b8 * iStack_168bc];
      }
    }
  }
  iStack_168b0 = 0;
  *(undefined8 *)(puVar7 + -0x18d8) = 0x102641;
  pcStack_168a8 = (char *)malloc(1);
  *(undefined8 *)(puVar7 + -0x18d8) = 0x102652;
  pcStack_168a0 = (char *)malloc(1);
  *(undefined8 *)(puVar7 + -0x18d8) = 0x102668;
  puts(&DAT_00103018);
  *(undefined8 *)(puVar7 + -0x18d8) = 0x10267c;
  printf(&DAT_00103078);
  while( true ) {
    *(undefined8 *)(puVar7 + -0x18d8) = 0x1026cd;
    iVar3 = getchar();
    if ((char)iVar3 == '\n') break;
    pcStack_168a8[iStack_168b4] = (char)iVar3;
    *(undefined8 *)(puVar7 + -0x18d8) = 0x1026c1;
    pcStack_168a8 = (char *)realloc(pcStack_168a8,(long)(iStack_168b4 + 1));
    iStack_168b4 = iStack_168b4 + 1;
  }
  pcStack_168a8[iStack_168b4] = '\0';
  *(undefined8 *)(puVar7 + -0x18d8) = 0x102706;
  printf(&DAT_001030a0);
  while( true ) {
    *(undefined8 *)(puVar7 + -0x18d8) = 0x102757;
    iVar3 = getchar();
    if ((char)iVar3 == '\n') break;
    pcStack_168a0[iStack_168b0] = (char)iVar3;
    *(undefined8 *)(puVar7 + -0x18d8) = 0x10274b;
    pcStack_168a0 = (char *)realloc(pcStack_168a0,(long)(iStack_168b0 + 1));
    iStack_168b0 = iStack_168b0 + 1;
  }
  pcStack_168a0[iStack_168b0] = '\0';
  if ((*pcStack_168a8 == '\0') || (*pcStack_168a0 == '\0')) {
    *(undefined8 *)(puVar7 + -0x18d8) = 0x1027a7;
    puts(&DAT_001030c8);
  }
  else {
    *(undefined8 *)(puVar7 + -0x18d8) = 0x1027de;
    uVar5 = sum(pcStack_168a8,pcStack_168a0,apcStack_16878,0x3e,0x3e,local_f058);
    *(char ***)(puVar7 + -0x18e0) = local_7838;
    *(undefined8 *)(puVar7 + -0x18e8) = 0x102823;
    pcVar6 = (char *)multipl(pcStack_168a8,pcStack_168a0,apcStack_16878,0x3e,0x3e,local_f058);
    *(undefined8 *)(puVar7 + -0x18d8) = 0x102863;
    iVar3 = strcmp(pcVar6,"brightfutur3");
    if (iVar3 == 0) {
      *(undefined8 *)(puVar7 + -0x18d8) = 0x102899;
      pcVar6 = (char *)sum(uVar5,"gEH6bGRCgl",apcStack_16878,0x3e,0x3e,local_f058);
      *(undefined8 *)(puVar7 + -0x18d8) = 0x1028a1;
      puts(pcVar6);
    }
    else {
      *(undefined8 *)(puVar7 + -0x18d8) = 0x1028b2;
      puts(&DAT_00103168);
    }
  }





  if (canary != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    *(undefined8 *)(puVar7 + -0x18d8) = 0x1028cb;
    __stack_chk_fail();
  }
  return 0;
}
