$( ".post" ).each(function() {
    var card = $( this ).find( '.post-card' );
    var show = card.find('.show')
    var image = card.find( '.post-card__image' );
    var text = card.find( '.post-card__text' );
    var iheight = parseInt(image.css('height'));
    var theight = parseInt(text.css('height'));
    if (isNaN(theight)){
        var theight = 0;
    };
    if (isNaN(iheight)){
        var iheight = 0;
    };
    var cheight = iheight + theight;
    if(cheight <= 450){
        show.css('display', 'none')
    };
    if(cheight > 450){
        card.css('height', '450px')
    };
});

$( ".show" ).click(function() {
    var card = $( this ).parent();
    var image = card.find( '.post-card__image' );
    var text = card.find( '.post-card__text' );
    var iheight = parseInt(image.css('height'));
    var theight = parseInt(text.css('height'));
    if($( this ).parent().css('height') == '450px'){
        var text = $(this).text();
        text = text.replace('показать полностью', 'свернуть пост');
        $(this).text(text)
        $(this).parent().css('height', 'auto');
        if((iheight != 0) && (isNaN(theight))){
            $(this).css({'opacity': '0.4',
                         'bottom': '15px',
                        });
        } else {
            $(this).css({'opacity': '0.4',
                         'bottom': '10px',
                        });
            card.css('padding-bottom', '50px');
        }
    } else {
        var text = $(this).text();
        text = text.replace('свернуть пост', 'показать полностью');
        $(this).text(text)
        $(this).parent().css({'height': '450px',
                            });
        $(this).css({'opacity': '1',
                     'bottom': '0',
                    });
    }
});