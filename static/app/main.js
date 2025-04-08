// var swiper = new Swiper(".newsSwipper", {
//     pagination: {
//       el: ".swiper-pagination",
//       clickable: true,
//     },
//   });

var categoriesSwipper = new Swiper(".categoriesSwipper", {
  slidesPerView: 5,
  spaceBetween: 30,
});

function applyLanguageFromStorage() {
  var storedLanguage = localStorage.getItem("selectedLanguage");
  var storedFlag = localStorage.getItem("selectedFlag");

  if (storedLanguage && storedFlag) {
    $("#current_flag").attr("src", storedFlag);
    $("#current_flag").attr(
      "alt",
      storedLanguage === "en" ? "english" : "arabic"
    );
    $("#current_language").text(storedLanguage.toUpperCase());
  }
}

$(document).ready(function () {
  applyLanguageFromStorage();
  $(".phone_menu, .language").hide();

  $(".phone_items button").click(function (event) {
    event.stopPropagation();
    $(".phone_menu").slideToggle(200);
    $(".language").slideUp(200);
  });

  $(".language_menu button").click(function (event) {
    event.stopPropagation();
    $(".language").slideToggle(200);
    $(".phone_menu").slideUp(200);
  });

  $(".language a").click(function (event) {
    event.preventDefault();

    var selectedLanguage = $(this).data("language");
    var flagImage = $(this).data("flag");
    var flagAlt = selectedLanguage === "en" ? "english" : "arabic";
    var languageText = selectedLanguage.toUpperCase();

    $("#current_flag").attr("src", `/static/assets/flags/${flagImage}`);
    $("#current_flag").attr("alt", flagAlt);
    $("#current_language").text(languageText);

    localStorage.setItem("selectedLanguage", selectedLanguage);
    localStorage.setItem("selectedFlag", `/static/assets/flags/${flagImage}`);

    $("#language_input").val(selectedLanguage);

    $("#language_form").submit();
  });

  $(document).click(function () {
    $(".phone_menu, .language").slideUp(200);
  });

  $(".phone_menu, .language").click(function (event) {
    event.stopPropagation();
  });

  $("#catalog_main_toggle").click(function () {
    $(".catalog_content").toggleClass("active");
    $("svg").toggleClass("rotated");
  });
});

$(document).ready(function () {
  var hideTimeout;

  function createSubcategoryBlock(level) {
    var existingBlock = $(".subcategory-container[data-level='" + level + "']");
    if (existingBlock.length === 0) {
      var newBlock = $(
        "<div class='catalog_items_submenus subcategory-container' data-level='" +
          level +
          "'>" +
          "<div class='wrapper_list_submenus'><ul></ul></div></div>"
      );
      $(".catalog_content").append(newBlock);
    }
  }

  function fetchSubcategories(categoryId, level) {
    $.ajax({
      url: "/get-subcategories/",
      data: { category_id: categoryId },
      success: function (response) {
        if (response.subcategories.length > 0) {
          createSubcategoryBlock(level);
          var targetBlock = $(
            ".subcategory-container[data-level='" + level + "'] ul"
          );
          targetBlock.empty();

          $.each(response.subcategories, function (index, subcategory) {
            var subcategoryItem = $(
              "<li class='subcategory-item' data-category-id='" +
                subcategory.id +
                "'></li>"
            );
            var subcategoryLink = $(
              "<a href='/category/" +
                subcategory.slug +
                "/'>" +
                subcategory.name +
                "</a>"
            );

            if (subcategory.has_subcategories) {
              var arrowIcon = `<svg width="10" viewBox="0 0 9 6" fill="none" xmlns="http://www.w3.org/2000/svg">
                                                <path fill-rule="evenodd" clip-rule="evenodd" d="M7.06 0L4 3.05333L0.94 0L0 0.94L4 4.94L8 0.94L7.06 0Z" fill="#BDBFCD"></path>
                                             </svg>`;
              subcategoryLink.append(arrowIcon);
            }
            subcategoryItem.append(subcategoryLink);
            targetBlock.append(subcategoryItem);
          });

          $(".subcategory-container[data-level='" + level + "']").show();
        }
      },
      error: function () {
        console.log("Error fetching subcategories");
      },
    });
  }

  $(".parent-category").mouseenter(function () {
    var categoryId = $(this).data("category-id");
    clearTimeout(hideTimeout); // Cancel hide timeout when hovering
    fetchSubcategories(categoryId, 1);
  });

  $(document).on("mouseenter", ".subcategory-item", function () {
    var subcategoryId = $(this).data("category-id");
    var level = $(this).closest(".subcategory-container").data("level") + 1;
    clearTimeout(hideTimeout);
    fetchSubcategories(subcategoryId, level);
  });

  $(document).on("mouseenter", ".subcategory-container", function () {
    clearTimeout(hideTimeout);
  });

  $(document).on(
    "mouseleave",
    ".subcategory-container, .parent-category",
    function () {
      hideTimeout = setTimeout(function () {
        $(".subcategory-container").hide();
      }, 300); // Delay hiding for 300ms
    }
  );
});


