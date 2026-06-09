(function ($) {
	'use strict';

	$(window).on('load', function () {
		setTimeout(function () {
			$('#contact-form').off('submit').on('submit', function (e) {
				e.preventDefault();
				e.stopImmediatePropagation();

				const form = $(this);
				const btn = form.find('.btn-send');

				if (btn.prop('disabled')) return;
				btn.val('Sending...').prop('disabled', true);

				$.ajax({
					type: 'POST',
					url: form.attr('action'),
					data: form.serialize(),
					success: function (response) {
						const html = $(response);
						const successMsg = html.find('.alert-success');
						$('.messages').empty();
						if (successMsg.length) {
							$('.messages').html(
								'<div class="alert alert-success">Your message was sent successfully! We will get back to you soon.</div>'
							);
							form[0].reset();
						} else {
							$('#contact-form').html(html.find('#contact-form').html());
						}
						btn.val('Send message').prop('disabled', false);
					},
					error: function () {
						$('.messages').html(
							'<div class="alert alert-danger">Something went wrong. Please try again.</div>'
						);
						btn.val('Send message').prop('disabled', false);
					}
				});
			});
		}, 500);
	});

})(jQuery);