/**
 * @license Copyright (c) 2003-2014, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.md or http://ckeditor.com/license
 */

CKEDITOR.editorConfig = function( config ) {
	// Define changes to default configuration here. For example:
	// config.language = 'fr';
	// config.uiColor = '#AADC6E';
    //config.skin = 'office2013';
    //config.language = 'zh-cn';
    config.font_names='宋体/宋体;黑体/黑体;仿宋/仿宋_GB2312;楷体/楷体_GB2312;隶书/隶书;幼圆/幼圆;微软雅黑/微软雅黑;'+ config.font_names;
    config.enterMode = CKEDITOR.ENTER_DIV;
    config.shiftEnterMode = CKEDITOR.ENTER_BR;
    //config.filebrowserBrowseUrl = 'ckeditor/upload/?type=flash';
    //config.filebrowserImageBrowseUrl = 'kcfinder/browse.php?type=images';
    //config.filebrowserFlashBrowseUrl = 'kcfinder/browse.php?type=flash';
    //config.filebrowserUploadUrl = 'ckeditor/upload/?type=flash';
    //config.filebrowserImageUploadUrl = 'kcfinder/upload.php?type=images';
    //config.filebrowserFlashUploadUrl = 'kcfinder/upload.php?type=flash';
};
