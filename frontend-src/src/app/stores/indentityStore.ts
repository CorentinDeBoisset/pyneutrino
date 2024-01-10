import { Injectable } from "@angular/core";
import { BehaviorSubject } from "rxjs";
import { generateKey, readPrivateKey, readKey, decryptKey, KeyPair, SerializedKeyPair } from "openpgp";
import { LoginResponse, UserEntity } from "./types";

@Injectable({ providedIn: 'root' })
export class IdentityStore {
  private userSubject = new BehaviorSubject<UserEntity|null>(null)
  user$ = this.userSubject.asObservable()

  async initUserSession(passphrase: string, data: LoginResponse) {
    const publicKey = await readKey({ armoredKey: data.public_key });
    const privateKey = await decryptKey({
      privateKey: await readPrivateKey({ armoredKey: data.private_key }),
      passphrase: passphrase,
    });

    if (publicKey.getFingerprint() !== privateKey.getFingerprint()) {
      console.warn("The private and public PGP keys have mismatching fingerprints.")
    }

    // Store the user data in local storage
    window.localStorage.clear();
    window.localStorage.setItem("user_id", data.id);
    window.localStorage.setItem("user_email", data.email);
    window.localStorage.setItem("username", data.username);
    window.localStorage.setItem("user_private_key", JSON.stringify(privateKey.armor()));
    window.localStorage.setItem("user_public_key", JSON.stringify(publicKey.armor()));

    this.userSubject.next({
      id: data.id,
      email: data.email,
      username: data.username,
      publicKey: publicKey.armor(),
      privateKey: privateKey.armor(),
    });
  }

  initGuestSession(userId: string, keyPair: SerializedKeyPair<string>) {
    window.localStorage.setItem("guest_user_id", userId);
    window.localStorage.setItem("guest_public_key", JSON.stringify(keyPair.publicKey))
    window.localStorage.setItem("guest_private_key", JSON.stringify(keyPair.privateKey))
    this.userSubject.next({
      id: userId,
      email: "",
      username: "",
      publicKey: keyPair.publicKey,
      privateKey: keyPair.privateKey,
    })
  }

  restoreUserSession() {
    // this property is defined in the html by the server, since we cannot list httpOnly cookies from the JS
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    if (!(<any>window).hasSession) {
      window.localStorage.clear();
      this.userSubject.next(null);
      return
    }

    const userId = window.localStorage.getItem("user_id");
    const userEmail = window.localStorage.getItem("user_email");
    const username = window.localStorage.getItem("username");
    const privKey = JSON.parse(window.localStorage.getItem("user_private_key") || '""');
    const pubKey = JSON.parse(window.localStorage.getItem("user_public_key") || '""');

    if (userId === null || userEmail === null || username === null || privKey === null || pubKey === null) {
      // If there is not a standard logged in user, we try to load as a guest user
      const userId = window.localStorage.getItem("guest_user_id");
      const privKey = JSON.parse(window.localStorage.getItem("guest_public_key") || '""')
      const pubKey = JSON.parse(window.localStorage.getItem("guest_private_key") || '""')

      if (!userId || !privKey || !pubKey) {
        window.localStorage.clear();
        this.userSubject.next(null);
        return
      }

      this.userSubject.next({
        id: userId,
        email: "",
        username: "",
        publicKey: pubKey,
        privateKey: privKey,
      })

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

  getCurrentUser(): UserEntity|null {
    return this.userSubject.getValue();
  }

  isAuthenticated(): boolean {
    return (this.userSubject.value !== null)
  }

  logout() {
    window.localStorage.clear();
    this.userSubject.next(null);
  }

  async generatePgpKeyPair(email: string, username: string, passphrase: string) {
    const keyPair = await generateKey({
      type: "ecc",
      curve: "p256",
      keyExpirationTime: 3600 * 24 * 30 + 3600, // Default duration of a server session, plus a buffer to be safe
      userIDs: [{ name: username, email: email }],
      passphrase,
      format: "armored",
    });

    return keyPair;
  }
}
