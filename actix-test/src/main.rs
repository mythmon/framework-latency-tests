use std::{collections::HashMap, time::Duration};
use actix_web::{App, HttpResponse, HttpServer, Responder, web};
use tokio::sync::Mutex;

#[derive(Default)]
struct AppState{
    counters: Mutex<HashMap<String, u64>>
}

async fn incr<'a>(name: web::Path<String>, state: web::Data<AppState>) -> impl Responder {
    tokio::time::sleep(Duration::from_millis(10)).await;

    let name = name.into_inner();
    let new_value = {
        let mut counters = state.counters.lock().await;
        let entry = counters.entry(name.clone()).or_insert(0);
        *entry += 1;
        *entry
    };

    println!("Incremented {} to {}", name, new_value);

    HttpResponse::Ok().content_type("application/json").body(
    serde_json::to_string(&serde_json::json!({ &name: new_value })).unwrap())
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    let state = web::Data::new(AppState::default());

    HttpServer::new(move || {
        App::new()
            .app_data(state.clone())
            .route("/{name}", web::get().to(incr))
    })
    .workers(4)
    .bind(("127.0.0.1", 9201))?
    .run()
    .await
}
