export declare class Client {
    private baseURL;
    private token;
    private httpClient;
    constructor(config?: any);
    request(method: string, path: string, { query, body }?: {
        query?: any;
        body?: any;
    }): Promise<any>;
}
