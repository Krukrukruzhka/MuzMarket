
const linksListItem = document.querySelectorAll('.links__list-item');

const tabsBoxItem = document.querySelectorAll('.tabs-box__item');


if(linksListItem && tabsBoxItem) {


    linksListItem.forEach((tabBtn) => {
        tabBtn.addEventListener('click', () => {
            linksListItem.forEach((item) => {
                item.classList.remove('links__list-item--active');
            });
            tabsBoxItem.forEach((item) => {
                item.classList.remove('active--element');
            });
            const currentTab = document.querySelector(tabBtn.getAttribute('data-tab'));
            currentTab.classList.add('active--element');
            tabBtn.classList.add('links__list-item--active');
        });
    });
}

//=================================================================================
//Показать больше характеристик
//=================================================================================

const showMoreSpecificationsBtn = document.querySelector('.tabs-box__specifications-list-all');



if(showMoreSpecificationsBtn) {
    showMoreSpecificationsBtn.addEventListener('click', () => {
        const specificationWrapper = document.querySelector('.tabs-box__specifications-wrapper');

        if(specificationWrapper.classList.contains('tabs-box__specifications-wrapper--active') === false) {
            specificationWrapper.classList.add('tabs-box__specifications-wrapper--active');
            showMoreSpecificationsBtn.textContent = 'скрыть';
        }
        else {
            specificationWrapper.classList.remove('tabs-box__specifications-wrapper--active');
            showMoreSpecificationsBtn.textContent = 'показать больше';
        }
        
    });
}

