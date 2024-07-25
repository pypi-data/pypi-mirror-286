export default {
    template: "<div></div>",
    mounted() {
        this.keycloak = new Keycloak({
            url: this.url,
            realm: this.realm,
            clientId: this.clientId
        });

        this.keycloak.onTokenExpired = () => this.keycloak.updateToken();
        this.keycloak.init(this.initOptions);

        this.keycloak.onReady = (authenticated) => this.$emit("onReady", {'authenticated': authenticated});
    },
    methods: {
        token() {
            return this.keycloak.token;
        },
        tokenParsed() {
            return this.keycloak.tokenParsed;
        },
        refreshToken() {
            return this.keycloak.refreshToken;
        },
        authenticated() {
            return this.keycloak.authenticated;
        },
        login(options) {
            return this.keycloak.login(options);
        },
        logout(options) {
            return this.keycloak.logout(options);
        }
    },
    props: {
        url: String,
        realm: String,
        clientId: String,
        initOptions: Object
    }
};
