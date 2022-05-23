var steps_count = 0;
function add_row() {
    let lbl = document.createElement('label')
    lbl.setAttribute('name', 'lbl')
    lbl.className = "col-sm-2 col-form-label";
    steps_count = 1 + steps_count;
    let str = 'Шаг ' +  steps_count;
    lbl.innerHTML = '<h6>'+ str + '</h6>';

    let new_div = document.createElement('div')
    new_div.setAttribute('name', 'new_div')
    new_div.setAttribute('id', 'new_div')
    new_div.className = "col-sm-8";

    let new_text = document.createElement('textarea');
    new_text.setAttribute("name", "steps")
    new_text.setAttribute("type", "text")
    new_text.className = 'form-control';

    let space = document.createElement('br');
    space.setAttribute("name", "space")
    new_div.append(new_text)
    new_tags.append(lbl, new_div, space)
}

function del_row() {
    steps_count = steps_count - 1;
    let delLbl = document.querySelectorAll("label[name='lbl']")
    let delDiv = document.querySelectorAll("div[name='new_div']")
    let delText = document.querySelectorAll("textarea[name='steps']")
    let delSpace = document.querySelectorAll("br[name='space']")
    delLbl[delLbl.length - 1].remove()
    delDiv[delDiv.length - 1].remove()
    delText[delText.length - 1].remove()
    delSpace[delSpace.length - 1].remove()
}