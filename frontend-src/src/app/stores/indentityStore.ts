import { Injectable } from "@angular/core";
import { LoginResponse, UserEntity } from "./types";
import { BehaviorSubject } from "rxjs";

@Injectable({ providedIn: 'root' })
export class IdentityStore {
  private userSubject = new BehaviorSubject<UserEntity|null>(null)
  user$ = this.userSubject.asObservable()

  initUserSession(password: string, data: LoginResponse) {
    // TODO: Decrypt the private key using the password
    // Also, Check that the private key and public key match

    // Store the user data in local storage
    window.localStorage.clear();
    window.localStorage.setItem("user_id", data.id);
    window.localStorage.setItem("user_email", data.email);
    window.localStorage.setItem("username", data.username);
    window.localStorage.setItem("user_private_key", "");
    window.localStorage.setItem("user_public_key", data.public_key);

    this.userSubject.next({
      id: data.id,
      email: data.email,
      username: data.username,
      publicKey: data.public_key,
      privateKey: "",
    });
  }

  restoreUserSession() {
    // this property is defined in the html by the server, since we cannot list httpOnly cookies from the JS
    if (!(<any>window).hasSession) {
      window.localStorage.clear();
      return
    }

    const userId = window.localStorage.getItem("user_id");
    const userEmail = window.localStorage.getItem("user_email");
    const username = window.localStorage.getItem("username");
    const privKey = window.localStorage.getItem("user_private_key");
    const pubKey = window.localStorage.getItem("user_public_key");

    if (userId === null || userEmail === null || username === null || privKey === null || pubKey === null) {
      window.localStorage.clear();
      return
    }

    // TODO: check the key pair

    this.userSubject.next({
      id: userId,
      email: userEmail,
      username: username,
      publicKey: pubKey,
      privateKey: privKey,
    })
  }

  isAuth(): boolean {
    return (this.userSubject.value !== null)
  }

  // generatePgpKeyPair() {
    // TODO: use protonmail's openPGP lib to create a key pair.
    // Then, store the keys in this.user
  // }
}
