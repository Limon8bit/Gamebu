$( '.fileInput' ).change(function() {
    var text = $('.image_input').text();
    if(($( this ).val() != "")){
        text = text.replace( 'Добавить картинку', $( this ).val());
        $('.image_input').text(text);
    } else {
        text = text.replace( $('.image_input').text(), 'Добавить картинку' );
        $('.image_input').text(text);
    }
    if ($('.image_input').text() != $('.fileInput').val()){
        text = text.replace( $('.image_input').text(), $('.fileInput').val() );
        $('.image_input').text(text);
    }
});
