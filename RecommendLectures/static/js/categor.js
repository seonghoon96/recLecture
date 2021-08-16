const checkBoxList = ['', '', '', '', ''];
let checkCount = 0;
let selectedPart = '';


function print(e) {
       console.log(e);
       console.log(e.innerHTML);
}

function sel(e){
        selectedPart = e.value; // 해당 버튼의 구분 return
        alert(selectedPart)
        const category = document.querySelector('.resv-wrapper');
        category.classList.add('open');
}

function closeCategory() {
    resetCheckBox();
    const category = document.querySelector('.resv-wrapper');
    category.classList.remove('open');
}

function showRecommendList(){
    closeCategory();
    resetCheckBox();
    var search_key = selectedPart
        $.ajax({
                url:'RecommendLectures/',

                data : {"input" : search_key},
                type : "GET",
                dataType : "json",
                success:function(result){
                        alert(result);
                        $("#tableset").text("성공");
                }
        });
    const lecturelist = document.querySelector('.lec-wrapper');
    lecturelist.classList.add('open');
}

function closeRecommendList() {
    const lecturelist = document.querySelector('.lec-wrapper');
    lecturelist.classList.remove('open');
    resetCheckBox();
}

function checkbox(box){
    if(box.checked == true)
    {
        checkBoxList[checkCount] = box.value;
        checkCount++;
    }
    console.log(checkBoxList, checkCount);
}

function resetCheckBox() {
    for(let i=0; i<checkCount; i++){
        const checkedBox = checkBoxList[i];
        const eraseBox = document.getElementById(checkedBox);
        eraseBox.checked = false;
    }
}

