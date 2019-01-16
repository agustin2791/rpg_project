let body = document.getElementsByTagName('body')[0];

function block_confirm() {
    
    let overlay = document.createElement('div');
    overlay.className = 'block-overlay';
    let container = document.createElement('div');
    let spin = document.createElement('div');
    let check = document.createElement('span');

    container.className = 'conf-container';
    check.className = 'far fa-check-circle fa-9x';
    spin.className = 'block-confirm';

    // for (let i = 1; i <= 360; i++) {
    //     setTimeout(function() {
    //         spin.style.opacity = ((i +1) * 2) / 100;
    //         spin.style.transform = 'translate(-50%, -50%) rotate(' + i +'deg)';
    //     }, 1);
    // }
    for (let i = 0; i < 3; i++) {
        let pill = document.createElement('div');
        pill.className = 'pill';
        container.appendChild(pill);
    }
    setTimeout(function() {
        let pills = document.getElementsByClassName('pill');
        for (let i = 0; i < pills.length; i++) {
            pills[i].style.opacity = 1;
        }
        setTimeout(function() {
            let pills = document.getElementsByClassName('pill');
            for (let i = 0; i < pills.length; i++) {
                pills[i].style.opacity = 0;
            }
        }, 250)
    }, 500)
    

    spin.appendChild(check);
    container.appendChild(spin);
    overlay.appendChild(container);
    body.appendChild(overlay);
    
    setTimeout(function() {
        overlay.style.opacity = 0;
    }, 1000);
    setTimeout(function() {
        body.removeChild(overlay);
    },1500);
}