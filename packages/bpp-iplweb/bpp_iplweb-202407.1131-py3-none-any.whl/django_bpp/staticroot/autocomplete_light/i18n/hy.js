/*! Select2 4.1.0-rc.0 | https://github.com/select2/select2/blob/master/LICENSE.md */
var dalLoadLanguage=function(n){var e;(e=n&&n.fn&&n.fn.select2&&n.fn.select2.amd?n.fn.select2.amd:e).define("select2/i18n/hy",[],function(){return{errorLoading:function(){return"Արդյունքները հնարավոր չէ բեռնել։"},inputTooLong:function(n){return"Խնդրում ենք հեռացնել "+(n.input.length-n.maximum)+" նշան"},inputTooShort:function(n){return"Խնդրում ենք մուտքագրել "+(n.minimum-n.input.length)+" կամ ավել նշաններ"},loadingMore:function(){return"Բեռնվում են նոր արդյունքներ․․․"},maximumSelected:function(n){return"Դուք կարող եք ընտրել առավելագույնը "+n.maximum+" կետ"},noResults:function(){return"Արդյունքներ չեն գտնվել"},searching:function(){return"Որոնում․․․"},removeAllItems:function(){return"Հեռացնել բոլոր տարրերը"}}}),e.define,e.require},event=new CustomEvent("dal-language-loaded",{lang:"hy"});document.dispatchEvent(event);