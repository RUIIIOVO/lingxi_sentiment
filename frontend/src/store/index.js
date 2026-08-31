import { createStore } from 'vuex'
import Cookies from "js-cookie";

export default createStore({
    state: {
        title: Cookies.get("title"),
        user_id: Cookies.get("user_id"),
        username: Cookies.get("username"),
    },
    mutations: {
        updateTitle(state, newTitle) {
            state.title = newTitle;
            Cookies.set("title", newTitle, { expires: 30 });
        },
        updateUserId(state, newUserId) {
            state.user_id = newUserId;
            // 存入cookie
            Cookies.set("user_id", newUserId, { expires: 30 });
        },
        updateUserName(state, newUserName) {
            state.username = newUserName;
            // 存入cookie
            Cookies.set("username", newUserName, { expires: 30 });
        }
    },
})
