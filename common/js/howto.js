// ゲーム共通の「遊び方」パネル
//
// 使い方(ゲーム側に書くのはこの2つだけ):
//   1. 文章を HTML に直接書く。ボタンを置きたい親要素(#game など)の中に入れる
//        <section class="howto" hidden><h2>遊び方</h2><p>...</p></section>
//   2. </body> の直前で読み込む
//        <script src="/common/js/howto.js" defer></script>
//
// 任意の調整:
//   - ボタンの位置: section に data-pos="top-left"(既定)/ top-right / bottom-left / bottom-right
//   - 既存のメニューに入れる: section に data-pos="none" を書き(浮かせるボタンを作らない)、
//     メニューの中の好きな要素に data-howto-open を付ける(JS で後から作った要素でもよい)
//   - プレイ中だけ浮かせるボタンを隠す:
//     document.documentElement.toggleAttribute('data-howto-hidden', プレイ中か)
//   - 色: ゲームの :root に --howto-bg / --howto-fg を書く
//
// 文章は JS で作らず HTML に残す(クローラーが JS を実行しなくても読めるようにするため)。
(() => {
  'use strict';

  const section = document.querySelector('section.howto');
  if (!section) return;

  // ---------- 見た目 ----------
  const style = document.createElement('style');
  style.textContent = `
    .howto-open{
      position:absolute;z-index:1000;min-width:44px;height:44px;padding:0 14px;margin:0;border:0;border-radius:22px;
      font:bold 13px/1 "Hiragino Sans","Hiragino Kaku Gothic ProN","Yu Gothic","Noto Sans JP",system-ui,sans-serif;
      background:var(--howto-bg,#181818);color:var(--howto-fg,#eee);box-shadow:0 2px 8px rgba(0,0,0,.15);
      cursor:pointer;touch-action:manipulation;
    }
    html[data-howto-hidden] .howto-open{display:none}
    .howto-open[data-pos="top-left"]{top:calc(env(safe-area-inset-top,0px) + 10px);left:calc(env(safe-area-inset-left,0px) + 10px)}
    .howto-open[data-pos="top-right"]{top:calc(env(safe-area-inset-top,0px) + 10px);right:calc(env(safe-area-inset-right,0px) + 10px)}
    .howto-open[data-pos="bottom-left"]{bottom:calc(env(safe-area-inset-bottom,0px) + 10px);left:calc(env(safe-area-inset-left,0px) + 10px)}
    .howto-open[data-pos="bottom-right"]{bottom:calc(env(safe-area-inset-bottom,0px) + 10px);right:calc(env(safe-area-inset-right,0px) + 10px)}
    .howto-dialog{
      width:min(calc(100vw - 32px),420px);max-height:calc(100dvh - 48px);padding:0;border:0;border-radius:16px;
      font:15px/1.7 "Hiragino Sans","Hiragino Kaku Gothic ProN","Yu Gothic","Noto Sans JP",system-ui,sans-serif;
      background:var(--howto-bg,#181818);color:var(--howto-fg,#eee);box-shadow:0 12px 32px rgba(0,0,0,.25);
    }
    .howto-dialog[open]{display:flex;flex-direction:column}
    .howto-dialog::backdrop{background:rgba(0,0,0,.5)}
    .howto-dialog .howto{
      flex:1 1 auto;min-height:0;overflow-y:auto;overscroll-behavior:contain;touch-action:pan-y;padding:24px 24px 8px;
      -webkit-user-select:text;user-select:text;
    }
    .howto-dialog h2{margin:20px 0 4px;font-size:16px;line-height:1.4}
    .howto-dialog h2:first-child{margin-top:0}
    .howto-dialog p{margin:0}
    .howto-dialog .howto-home{margin-top:12px}
    .howto-dialog .howto-home a{display:inline-block;padding:10px 0;color:inherit;font-weight:bold;text-decoration:underline}
    .howto-close{
      flex:none;display:block;width:calc(100% - 48px);min-height:44px;margin:12px 24px 20px;padding:0;
      border:1px solid currentColor;border-radius:22px;background:transparent;color:inherit;
      font:bold 15px/1 "Hiragino Sans","Hiragino Kaku Gothic ProN","Yu Gothic","Noto Sans JP",system-ui,sans-serif;
      cursor:pointer;touch-action:manipulation;
    }
  `;
  document.head.appendChild(style);

  // ---------- 部品 ----------
  // 既存のメニューに入れるゲーム(data-pos="none")では浮かせるボタンを作らない
  let openBtn = null;
  if (section.dataset.pos !== 'none') {
    openBtn = document.createElement('button');
    openBtn.type = 'button';
    openBtn.className = 'howto-open';
    openBtn.dataset.howtoOpen = '';
    openBtn.dataset.pos = section.dataset.pos || 'top-left';
    openBtn.textContent = '遊び方';
  }

  // <dialog> の showModal は最前面に出て背景も操作不能にするので、ゲームごとの z-index に左右されない
  const dialog = document.createElement('dialog');
  dialog.className = 'howto-dialog';
  dialog.setAttribute('aria-label', '遊び方');

  const closeBtn = document.createElement('button');
  closeBtn.type = 'button';
  closeBtn.className = 'howto-close';
  closeBtn.textContent = '閉じる';

  if (openBtn) section.parentNode.insertBefore(openBtn, section);
  section.hidden = false;
  dialog.append(section, closeBtn);
  document.body.appendChild(dialog);

  // ---------- 開閉 ----------
  // メニューの要素は後から作られることがあるので document で受ける。
  // ゲーム側が click を止めていても届くようキャプチャで拾う
  document.addEventListener('click', e => {
    if (!dialog.open && e.target.closest?.('[data-howto-open]')) dialog.showModal();
  }, true);
  closeBtn.addEventListener('click', () => dialog.close());
  // 閉じるとフォーカスが開いたボタンに戻り、PC のスペースや Enter がゲームに届かず再び開いてしまうので外す
  dialog.addEventListener('close', () => document.activeElement?.blur());
  // 枠の外(背景)を押しても閉じる。文字を選択するドラッグが枠の外で終わった場合は閉じない
  let downOnBackdrop = false;
  dialog.addEventListener('pointerdown', e => { downOnBackdrop = e.target === dialog; });
  dialog.addEventListener('click', e => { if (downOnBackdrop && e.target === dialog) dialog.close(); });

  // パネルとボタンの操作がゲーム側に届くと、裏でゲームが進んだりリスタートしたりするので止める
  const STOP = [
    'pointerdown', 'pointermove', 'pointerup', 'pointercancel',
    'mousedown', 'mousemove', 'mouseup',
    'touchstart', 'touchmove', 'touchend', 'touchcancel',
    'click', 'wheel', 'contextmenu', 'selectstart', 'keydown', 'keyup',
  ];
  for (const el of [openBtn, dialog]) {
    if (!el) continue;
    for (const type of STOP) el.addEventListener(type, e => e.stopPropagation());
  }
})();
