//@ts-check

export class Utils {
  /**
   * Gets date as string.
   *
   * @returns {string}
   */
  static getDateAsString() {
    let date = new Date();
    let year = date.getFullYear();
    let month = date.getMonth() + 1;
    let day = date.getDate();
    let hours = date.getHours();
    let minutes = date.getMinutes();
    let seconds = date.getSeconds();

    return (
      year +
      '-' +
      month +
      '-' +
      day +
      ' ' +
      hours +
      ':' +
      minutes +
      ':' +
      seconds
    );
  }

  static resizeChatFrame() {
    let chatFrame = document.getElementById('chatFrame');
    let chatInner = document.getElementById('chatInner');
    let msgsView = document.getElementById('msgsView');
    let composeMsg = document.getElementById('composeMsg');

    chatInner.style.height = window.innerHeight - chatFrame.offsetTop + 'px';
    msgsView.style.height =
      chatInner.offsetHeight -
      composeMsg.offsetHeight -
      targetUser.offsetHeight +
      'px';
  }

  static getTargetUsername() {
    let targetUser = $(event.target).text();

    if ($(event.target).hasClass('inbox_last_msg'))
      targetUser = $($($(event.target).parent()).children()[0]).text();
    else if ($(event.target).hasClass('inbox_user'))
      targetUser = $($(event.target).children()[0]).text();

    return targetUser;
  }

  static setToAdded(eSrc) {
    $(eSrc).addClass('contact_added');
    $(eSrc).text('Added');
    $(eSrc).css('margin-right', 0 + 'px');
    $(eSrc).css('margin-top', 2 + 'px');
  }
}

window.Utils = Utils;
