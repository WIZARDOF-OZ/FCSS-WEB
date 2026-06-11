
(function ($) {
    'use strict';
    $(document).ready(function () {
        $('#newsletter-btn').on('click', function () {
            var email = $('#newsletter-email').val().trim();
            var msgBox = $('#newsletter-message');
            var btn = $(this);

            if (!email) {
                msgBox.html('<div class="alert alert-danger" style="padding:8px;">Please enter your email.</div>').show();
                return;
            }

            btn.prop('disabled', true).html('<i class="fa fa-spinner fa-spin"></i>');

            $.ajax({
                type: 'POST',
                url: "{% url 'newsletter-subscribe' %}",
                data: {
                    email: email,
                    csrfmiddlewaretoken: '{{ csrf_token }}'
                },
                success: function (response) {
                    if (response.status === 'success') {
                        msgBox.html('<div class="alert alert-success" style="padding:8px;">' + response.message + '</div>').show();
                        $('#newsletter-email').val('');
                    } else {
                        msgBox.html('<div class="alert alert-danger" style="padding:8px;">' + response.message + '</div>').show();
                    }
                    btn.prop('disabled', false).html('<i class="fa fa-arrow-right"></i>');

                    // Hide message after 4 seconds
                    setTimeout(function () { msgBox.hide(); }, 4000);
                },
                error: function () {
                    msgBox.html('<div class="alert alert-danger" style="padding:8px;">Something went wrong. Please try again.</div>').show();
                    btn.prop('disabled', false).html('<i class="fa fa-arrow-right"></i>');
                }
            });
        });

        // Also trigger on Enter key
        $('#newsletter-email').on('keypress', function (e) {
            if (e.which === 13) $('#newsletter-btn').click();
        });
    });




})(jQuery);