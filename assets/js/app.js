//今日の日付
//いったん削除
//https://www.sejuku.net/blog/88958
//
function checkPerGroup (idAndClass) {
  let checkAll = document.getElementById(idAndClass);
  let checks = document.getElementsByClassName(idAndClass);
  
  const funcCheckAll = (bool) => {
      for (let i = 0; i < checks.length; i++) {
          checks[i].checked = bool;
      }
  }
  const funcCheck = () => {
      let count = 0;
      for (let i = 0; i < checks.length; i++) {
          if (checks[i].checked) {
              count += 1;
          }
      }
  
      if (checks.length === count) {
          checkAll.checked = true;
      } else {
          checkAll.checked = false;
      }
  };
  
  checkAll.addEventListener("click",() => {
      funcCheckAll(checkAll.checked);
  },false);
  
  for (let i = 0; i < checks.length; i++) {
      checks[i].addEventListener("click", funcCheck, false);
  }
}

checkPerGroup("gen0JP")
checkPerGroup("gen1JP")
checkPerGroup("gen2JP")
checkPerGroup("gameJP")
checkPerGroup("gen3JP")
checkPerGroup("gen4JP")
checkPerGroup("gen5JP")
checkPerGroup("holoX")
checkPerGroup("myth")
checkPerGroup("projectHOPE")
checkPerGroup("council")
checkPerGroup("gen1ID")
checkPerGroup("gen2ID")
checkPerGroup("gen3ID")
checkPerGroup("IDall")
checkPerGroup("ENall")
checkPerGroup("JPall")
checkPerGroup("HOLOall")





