$(document).on('click', '.number-spinner button', function () {
    var btn = $(this),
        oldValue = btn.closest('.number-spinner').find('input').val().trim(),
        newVal = 0,
        oldPrice = btn.closest('.basket-item').find('.item-price').text().trim().split(' ')[0],
        newPrice = 0,
        oldPriceOfItems = parseInt(document.getElementById("price-of-items").textContent),
        oldTotalPrice = parseInt(document.getElementById("total-price").textContent),
        newPriceOfItems = 0,
        newTotalPrice = 0;

    if (btn.attr('data-dir') === 'up') {
        newVal = parseInt(oldValue) + 1;
    } else {
        if (oldValue > 1) {
            newVal = parseInt(oldValue) - 1;
        } else {
            newVal = 1;
        }
    }
    newPrice = parseInt(oldPrice) / parseInt(oldValue) * newVal
    newPriceOfItems = oldPriceOfItems - parseInt(oldPrice) + newPrice
    newTotalPrice = oldTotalPrice - oldPriceOfItems + newPriceOfItems

    btn.closest('.number-spinner').find('input').val(newVal)
    btn.closest('.basket-item').find('.item-price').text(newPrice + ' ₽')
    document.getElementById("price-of-items").textContent = newPriceOfItems + ' ₽'
    document.getElementById("total-price").textContent = newTotalPrice + ' ₽'
});

$(document).on('click', '.btn-trash-can button', function () {
    let alertsList = document.getElementsByClassName("alerts-list"),
        alertItem = document.createElement("div"),
        span = document.createElement("div"),
        text = document.createTextNode("Товар удален из корзины"),
        closeButton =document.createElement("button"),
        closeIcon =document.createElement("img"),
        btn = $(this),
        basketItem = btn.closest(".basket-item"),
        priceOfItem = parseInt(btn.closest('.basket-item').find('.item-price').text().trim().split(' ')[0]),
        priceOfItems = parseInt(document.getElementById("price-of-items").textContent),
        totalPrice = parseInt(document.getElementById("total-price").textContent)

    basketItem.remove()
    priceOfItems -= priceOfItem
    totalPrice -= priceOfItem

    document.getElementById("price-of-items").textContent = priceOfItems + ' ₽'
    document.getElementById("total-price").textContent = totalPrice + ' ₽'

    alertItem.className = "alert-item"
    closeIcon.src = "/chocolate-factory/src/resources/close-svgrepo-com.svg"
    closeButton.className = "btn shadow-none"
    span.appendChild(text)
    closeButton.appendChild(closeIcon)
    alertItem.appendChild(span)
    alertItem.appendChild(closeButton)
    alertsList.item(0).appendChild(alertItem)

    alertItem.classList.add("disappear")

    setTimeout(function () {
        alertItem.remove()
    }, 4000)
})